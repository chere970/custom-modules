from odoo import fields,models, api

class Employee(models.Model):
    _inherit='res.partner'
    
    employee_code=fields.Char(string="Employee Code: ")
    is_employee=fields.Boolean(string="Emplyee ?", default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
    # Your code here
    
       records=super().create(vals_list)
       
       return records