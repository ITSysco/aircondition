# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class CancelAppointment(models.TransientModel):
    _name = 'cancel.appointment'
    _description = 'Cancel Appointment'
    _rec_name = "appointment_id"

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', 
                                    domain=[('priority', 'in', ('0', '1', False)), '|',
                                            ('state', '=', 'draft'), ('state', '=', 'in_progress')])
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string='Cancellation Date')

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointment, self).default_get(fields)
        res['cancel_date'] = datetime.date.today()
        res['appointment_id'] = self.env.context.get('active_id')
        return res

    def action_cancel(self):
        if self.appointment_id.booking == fields.Date.today():
            raise ValidationError(_("Cancelling of same date booking not allowed"))
        else:
            self.appointment_id.state = 'cancel'
