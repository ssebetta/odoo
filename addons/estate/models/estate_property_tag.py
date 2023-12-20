from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate_property_tags"
    _description="Tags of properties in estate"

    name = fields.Char('Name', required=True)

    _sql_constraints_ = [
        ('name_unique', 'unique(name)', "Tag name must be unique!"),
    ]
