from odoo import fields, models

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
