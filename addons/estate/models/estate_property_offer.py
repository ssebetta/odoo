from datetime import timedelta, datetime
from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name="estate_property_offers"
    _description="Offers on properties in estate"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'),('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Potential Buyer")
    property_id = fields.Many2one("estate_property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

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
