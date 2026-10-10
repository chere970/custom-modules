from datetime import timedelta
from odoo import fields
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, AccessError


class TestTodoTask(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.todo_user = cls.env['res.users'].create({
            'name': 'Todo Test User',
            'login': 'todo_user_test',
            'groups_id': [(6, 0, [cls.env.ref('tolo_todo.group_todo_user').id])],
        })
        cls.todo_manager = cls.env['res.users'].create({
            'name': 'Todo Test Manager',
            'login': 'todo_manager_test',
            'groups_id': [(6, 0, [cls.env.ref('tolo_todo.group_todo_manager').id])],
        })

    def test_workflow_transitions(self):
        task = self.env['todo.task'].with_user(self.todo_user).create({
            'name': 'Test Workflow Task',
        })
        self.assertEqual(task.state, 'draft')

        task.action_start()
        self.assertEqual(task.state, 'in_progress')

        task.action_done()
        self.assertEqual(task.state, 'done')

    def test_cancel_permissions(self):
        # User can cancel in draft
        task = self.env['todo.task'].with_user(self.todo_user).create({'name': 'Draft Task'})
        task.action_cancel()
        self.assertEqual(task.state, 'cancelled')

        # In-progress task cancellation
        task2 = self.env['todo.task'].with_user(self.todo_user).create({'name': 'In Progress Task'})
        task2.action_start()

        # Regular user cannot cancel in_progress
        with self.assertRaises(UserError):
            task2.with_user(self.todo_user).action_cancel()

        # Manager can cancel in_progress
        task2.with_user(self.todo_manager).action_cancel()
        self.assertEqual(task2.state, 'cancelled')

    def test_overdue_logic(self):
        yesterday = fields.Date.context_today(self.env.user) - timedelta(days=1)
        task = self.env['todo.task'].create({
            'name': 'Overdue Task',
            'date_deadline': yesterday,
            'state': 'in_progress',
        })
        self.assertTrue(task.is_overdue)

        task.action_done()
        self.assertFalse(task.is_overdue)