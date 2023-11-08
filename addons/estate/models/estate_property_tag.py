from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate_property_tags"
    _description="Tags of properties in estate"

    name = fields.Char(required=True)
