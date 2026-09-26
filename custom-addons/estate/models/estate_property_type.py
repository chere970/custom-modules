from odoo import fields, models

class PropertyType(models.Model):
    _name="estate_property_type"
    _description="test"
    
    
    name=fields.Char(string="Name")