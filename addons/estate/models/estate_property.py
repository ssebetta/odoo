from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

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
    state = fields.Selection(
        string='Status',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),],
        default='new'
    )
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
    offer_ids = fields.One2many("estate_property_offers", "property_id")
    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price < 0)', 'The expected price cannot be negative.'),
        ('check_selling_price', 'CHECK(selling_price < 0)', 'The selling price cannot be negative.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0.00
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden is True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel_offer(self):
        for record in self:
            record.state = "canceled"
        return True
    
    def action_sell_property(self):
        for record in self:
            if record.state != "canceled": 
                record.state = "sold"
            else:
                raise UserError(_('Canceled properties cannot be sold'))
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9 and not float_is_zero(record.selling_price, precision_digits=2):
                raise ValidationError("Selling price should be atleast 90% of expected price")

