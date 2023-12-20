from datetime import timedelta, datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name="estate_property_offers"
    _description="Offers on properties in estate"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('new', 'New'),('accepted', 'Accepted'),('refused', 'Refused')],
        default="new",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Potential Buyer")
    property_id = fields.Many2one("estate_property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price < 0)',
         'Offer price cannot be negative.')   
    ]

    @api.depends('create_date', 'validity', 'property_id')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=+record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=+record.validity)
    
    def _inverse_deadline(self):
        for record in self:
            d1 = record.create_date
            d2 = record.date_deadline
            d3 = datetime.now()
            if d3:
                record.validity = abs((
                    datetime.strptime(d1.strftime("%Y-%m-%d"), "%Y-%m-%d") - \
                        datetime.strptime(d2.strftime("%Y-%m-%d"), "%Y-%m-%d")).days)
            else:
                record.validity = abs((
                    datetime.strptime(d3.strftime("%Y-%m-%d"), "%Y-%m-%d") - \
                        datetime.strptime(d2.strftime("%Y-%m-%d"), "%Y-%m-%d")).days)
    
    def action_confirm(self):
        for record in self:
            if not record.property_id.selling_price:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id
            else:
                raise UserError(_('An offer was already accepted.'))
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = "refused"
            if record.property_id.partner_id == record.partner_id:
                record.property_id.selling_price = 0.00
                record.property_id.partner_id = None
        return True
