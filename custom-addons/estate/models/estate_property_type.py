from odoo import fields, models

class PropertyType(models.Model):
    _name="estate.property.type"
    _description="test"
    
    
    name=fields.Char(string="Name")
    real_state_ids=fields.One2many("real.estate","property_type_id")