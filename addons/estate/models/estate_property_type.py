from odoo import fields, models

class EstatePropertyType(models.Model):
    _name="estate_property_type"
    _description="Types of properties in estate"

    name = fields.Char('Name', required=True)

    _sql_constraints_ = [
        ('name_unique', 'unique(name)', "Property Type name must be unique!"),
    ]