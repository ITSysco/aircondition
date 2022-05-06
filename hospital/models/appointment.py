# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
   _name = 'hospital.appointment'
   _inherit = ['mail.thread','mail.activity.mixin']
   _description = 'Hospital Appointment'
   _rec_name = 'patient_id'

   patient_id = fields.Many2one('hospital.patient', string='Patient',  ondelete='cascade', tracking=True)
   appointment_time =fields.Datetime(string="Appointment", default=fields.Datetime.now(), tracking=True)
   booking = fields.Date(string='Booking', default=fields.Date.today())
   gender = fields.Selection(related='patient_id.gender')
   ref = fields.Char(string='Reference')
   prescription = fields.Html(string='Prescription')
   priority = fields.Selection([('0', 'Normal'), 
                              ('1', 'Low'),
                              ('2', 'High'),
                              ('3', 'Very High')],
                              string="Priority", tracking=True)
   state = fields.Selection([('draft', 'Draft'), 
                           ('in_progress', 'In progress'),
                           ('done', 'Done'),
                           ('cancel', 'Cancelled')],
                           string="Status", default='draft', required=True, tracking=True)
   medicin_ids = fields.One2many('appointment.pharmcy', 'appointment_id', string='Medicin', tracking=True)
   hide_price = fields.Boolean(string='Hide Price', default=True)

   @api.onchange('patient_id')
   def onchange_patient_id(self):
      self.ref = self.patient_id.ref

   def action_name(self):
      return {
            'effect': {
            'fadeout': 'slow',
            'message': 'hello Geha How are you!',
            'type': 'rainbow_man',
            }
      }

   def action_cancel(self):
      action = self.env.ref('hospital.cancel_appointment_action_window').read()[0]
      return action

   def unlink(self):
      if self.state not in ['cancel', 'draft']:
            raise ValidationError(_("You are allowed to remove only draft and cancelled appointments"))
      return super(HospitalAppointment, self).unlink()



class Pharmcy(models.Model):
   _name = "appointment.pharmcy"
   _inherit = ['mail.thread','mail.activity.mixin']
   _description = "Pharmcy"
   _rec_name = 'product_id'

   product_id = fields.Many2one('product.product', string='Medicin', required=True, tracking=True)
   price = fields.Float(string='Price', tracking=True)
   qut = fields.Integer(string='Quantity', default=1, tracking=True)
   appointment_id = fields.Many2one('hospital.appointment', string='appo')
   total = fields.Float(string="Total Amount", compute='_compute_total')

   @api.depends('qut','price')
   def _compute_total(self):
      for s in self:
            s.total = s.price * s.qut

   @api.onchange('product_id')
   def onchange_product_id(self):
      self.price = self.product_id.list_price


