from odoo import fields, models


class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'

    name = fields.Char(
        string='Name',
        required=True
    )

    student_number = fields.Char(
        string='Student Number',
        required=True
    )

    email = fields.Char(
        string='Email'
    )

    age = fields.Integer(
        string='Age'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )
    phone=fields.Char(string="Phone")
