from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")  # Enables colorful pill badges in the UI

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The tag name must be unique!"),
    ]