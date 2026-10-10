# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ToloTodoTask(models.Model):
    _name = "tolo.todo.task"
    _description = "Tolo Todo Task"
    _order = "deadline asc, priority desc, id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="draft",
        required=True,
    )
    assignee_id = fields.Many2one("res.users", string="Assignee")
    deadline = fields.Datetime()
    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
        ],
        default="1",
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

    @api.depends("deadline", "state")
    def _compute_is_overdue(self):
        now=fields.Datetime.now()
        # TODO: replace this stub with correct logic
        for task in self:
            task.is_overdue = bool(
                task.deadline
                and task.deadline < now
                and task.state != "done"
            )
