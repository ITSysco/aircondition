# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = ['res.config.settings']

    cancel_days = fields.Integer(string='Delay alert contract outdated', 
                                default=5, config_parameter='hospital.cancel_days')
    hospital_type = fields.Selection(string='Hospital Type', selection=[('main', 'Main'),
                                                                        ('sucond', 'Sucond'),
                                                                        ('test', 'Test'),
                                                                        ('dantes', 'Dantes')], 
                                    default='main', config_parameter='hospital_sel.cancel_days')