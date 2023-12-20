# -*- coding: utf-8 -*-
{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Technical',
    'summary': 'Estate mgt',
    'description': "Estate management module",
    'depends': [
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'menus/estates_menu.xml',
    ],
    'installable': True,
    'application': True
}