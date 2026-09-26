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
    )
    postcode = fields.Char()

    # Can either write the one line method in the field definition, or call a m
    date_availability = fields.Date()
    expected_price = fields.Float()
    best_offer = fields.Float()
    selling_price = fields.Float()

    description = fields.Text()   