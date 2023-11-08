from datetime import timedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'estate properties table'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: (fields.Date.today() + timedelta(days=+90)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')]
    )
    active = fields.Boolean()
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    partner_id = fields.Many2one("res.partner", string="Buyer")
    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        tracking=True,
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate_property_tags", string="Tags")
