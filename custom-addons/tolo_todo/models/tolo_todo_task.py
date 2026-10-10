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
    created_by=fields.Many2one("res.users",invisible=True)
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
        store=True,
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

    def action_done(self):
        for record in self:
            if record.state != 'in_progress':
                raise UserError("Only in-progress tasks can be marked as Done.")
            record.state = 'done'

    def action_cancel(self):
        is_manager = self.env.user.has_group('tolo_todo.group_todo_manager')
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