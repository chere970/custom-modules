# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError,ValidationError


class ToloTodoTask(models.Model):
    _name = "tolo.todo.task"
    _description = "Tolo Todo Task"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, deadline asc, id desc'
    # _order = "deadline asc, priority desc, id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
            ("cancelled","Cancelled")
        ],
        default="draft",
        required=True,
    )
    created_by=fields.Many2one("res.users")
    assignee_id = fields.Many2one("res.users", string="Assignee")
    deadline = fields.Date(string="Deadline" ,tracking=True)
    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3","Urgent")
        ],
        string="Priority",
        default="1",
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    # TODO: implement computed field is_overdue
    # Rules: deadline is set AND deadline < now AND state != "done"
    # Hint: @api.depends("deadline", "state") and fields.Datetime.now()
    is_overdue = fields.Boolean(
        string="Is Overdue",
        compute="_compute_is_overdue",
        search="_search_is_overdue",
        
        # TODO: choose store=True or False and be ready to explain why
    )

    # @api.depends("deadline", "state")
    # def _compute_is_overdue(self):
    #     now=fields.Datetime.now()
    #     # TODO: replace this stub with correct logic
    #     for task in self:
    #         task.is_overdue = bool(
    #             task.deadline
    #             and task.deadline < now
    #             and task.state != "done"
    #         )
            
    @api.depends('deadline', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.deadline and record.state in ('draft', 'in_progress'):
                record.is_overdue = record.deadline < today
            else:
                record.is_overdue = False

    def _search_is_overdue(self, operator, value):
        today = fields.Date.context_today(self)
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [
                ('deadline', '<', today),
                ('state', 'in', ['draft', 'in_progress']),
            ]
        return [
            '|',
            ('deadline', '>=', today),
            ('state', 'in', ['done', 'cancelled']),
        ]
    def action_start(self):
        for record in self:
            if record.state != 'draft':
                raise UserError("Only draft tasks can be moved to In Progress.")
            record.state = 'in_progress'

            # 1. Schedule the internal To-Do activity
            if record.assignee_id:
                record.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=record.deadline or fields.Date.context_today(self),
                    summary=f"Complete task: {record.name}",
                    user_id=record.assignee_id.id,
                )

            # 2. Dispatch real email to the assignee
            if record.assignee_id and record.assignee_id.email:
                record.message_post(
                    body=(
                        f"<p>Hello <b>{record.assignee_id.name}</b>,</p>"
                        f"<p>The task <b>{record.name}</b> has officially been moved to <b>In Progress</b>.</p>"
                        f"<p><b>Deadline:</b> {record.deadline or 'No deadline specified'}</p>"
                        f"<p>Please review and begin working on this item.</p>"
                    ),
                    subject=f"Task In Progress: {record.name}",
                    partner_ids=[record.assignee_id.partner_id.id],
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                    email_layout_xmlid='mail.mail_notification_light',
                )
    def action_done(self):
        for record in self:
            if record.state != 'in_progress':
                raise UserError("Only in-progress tasks can be marked as Done.")
            record.state = 'done'

    def action_cancel(self):
        is_manager = self.env.user.has_group('tolo_todo.group_tolo_todo_manager')
        for record in self:
            if record.state == 'draft':
                record.state = 'cancelled'
            elif record.state == 'in_progress':
                if not is_manager:
                    raise UserError("Only Todo Managers can cancel tasks that are already in progress.")
                record.state = 'cancelled'
            else:
                raise UserError("Done or already cancelled tasks cannot be cancelled.")

    def action_reset_draft(self):
        for record in self:
            if record.state != 'cancelled':
                raise UserError("Only cancelled tasks can be reset to draft.")
            record.state = 'draft'
            
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.assignee_id and record.assignee_id != self.env.user:
                record.message_notify(
                    partner_ids=record.assignee_id.partner_id.ids,
                    body=f"You have been assigned to new task: <b>{record.name}</b>",
                    subject="New Task Assigned",
                )
        return records

    def write(self, vals):
        # Notify chatter if assignee changes
        old_assignees = {rec.id: rec.assignee_id for rec in self}
        res = super().write(vals)
        if 'assignee_id' in vals:
            for record in self:
                old_assignee = old_assignees.get(record.id)
                new_assignee = record.assignee_id
                if new_assignee and new_assignee != old_assignee:
                    record.message_post(
                        body=f"Task reassigned from <b>{old_assignee.name if old_assignee else 'Unassigned'}</b> to <b>{new_assignee.name}</b>.",
                        subtype_xmlid='mail.mt_comment',
                    )
        return res