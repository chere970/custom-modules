from odoo import fields, models
from odoo.exceptions import UserError

class RealEstate(models.Model):
    _name= "real.estate"
    _description="Test model"
    
    active = fields.Boolean(default=True, invisible=True)
    name = fields.Char(required=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new"
    )
    postcode = fields.Char()
    
    def _default_date(self):
        return fields.Date.today()

    # Can either write the one line method in the field definition, or call a m
    date_availability = fields.Date(default=_default_date)
    company_id = fields.Many2one(
    "res.company", 
    string="Company", 
    default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
    "res.currency", 
    string="Currency", 
    related="company_id.currency_id", 
    readonly=True
    )
    expected_price = fields.Monetary()
    best_offer = fields.Float()
    selling_price = fields.Monetary(readonly=True)

    description = fields.Text()  
    bedroms=fields.Integer()
    living_area=fields.Integer() 
    fecades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    total_area=fields.Integer()
    garden_orientation=fields.Selection(
        [
            ("north","North"),
            ("south","South"),
            ("east","East"),
            ("west","West"),
        ],
    )
    code=fields.Char()
    phone=fields.Char()
    property_type_id=fields.Many2one("estate.property.type")
    # offer_ids=fields.One2many("estate.property.offer","property_id")
    
    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be set as sold.")
            record.state = "sold"
        return True

    def action_cancel(self):
        # for record in self:
        #     if record.state == "sold":
        #         raise UserError("A sold property cannot be canceled.")
        #     record.state = "canceled"
        # return True
        return {
            "type": "ir.actions.act_window",
            "name": "Cancel Property",
            "res_model": "estate.cancel.wizard",
            "view_mode": "form",
            "target": "new",  # 'new' tells Odoo to open in a pop-up modal window
            "context": {"default_property_id": self.id},
        }
    
    
from odoo import fields, models

class EstateCancelWizard(models.TransientModel):
    _name = "estate.cancel.wizard"
    _description = "Cancel Property Wizard"

    reason = fields.Text(string="Reason for Cancellation", required=True)

    def action_confirm_cancel(self):
        # Retrieve the property record ID that opened this wizard
        active_id = self.env.context.get("active_id")
        if active_id:
            property_record = self.env["real.estate"].browse(active_id)
            property_record.state = "canceled"
            # Append the reason to property description or a dedicated log field
            property_record.description = (
                f"{property_record.description or ''}\nCancellation Reason: {self.reason}"
            )
        return True