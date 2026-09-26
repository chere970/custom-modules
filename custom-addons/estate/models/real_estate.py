from odoo import fields, models

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
    expected_price = fields.Float()
    best_offer = fields.Float()
    selling_price = fields.Float(readonly=True)

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
    property_type_id=fields.Many2one("estate.property.type")