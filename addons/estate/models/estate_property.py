from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate_property'
    _description = 'estate properties table'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(digits=2, required=True)
    selling_price = fields.Float(digits=2)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'),('south', 'South'),('east', 'East'),('west', 'West')]
    )
