# -*- coding: utf-8 -*-

from datetime import date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
   _name = 'hospital.patient'
   _inherit = ['mail.thread','mail.activity.mixin']
   _description = 'Hospital Patient'

   name_id = fields.Many2one(string='Name', comodel_name='res.partner', tracking=True, required=True)
   age = fields.Integer(string='Age', compute='_compute_age', inverse='_compute_birth_day', search="_search_age")
   gender = fields.Selection(string='Gender', selection=[('male', 'Male'), ('female', 'Female')], tracking=True)
   ref = fields.Char(string='Reference', readonly=True, default="New")
   active = fields.Boolean(string='Active', default=True, tracking=True)
   responsible_id = fields.Many2one(string='Responsible', comodel_name='res.users', ondelete='set null', 
                                    default=lambda self: self.env.uid, tracking=True)
   dob = fields.Date(string="Day Of Birth")
   state = fields.Selection([('draft', 'Draft'), 
                           ('in_progress', 'In progress'),
                           ('done', 'Done'),
                           ('cancel', 'Cancelled')],
                           string="Status", default='draft', required=True, tracking=True)
   appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
   image = fields.Image(string="Image", related='name_id.image_1920')
   tag_ids = fields.Many2many('patient.tag', 'patient_tag_ref', 'patient_id_name', 'tag_id_name',
                              string="Tags")
   appointment_count = fields.Integer(string='Appointment Count',compute='_compute_appointment_count', store=True)
   appointments_ids = fields.One2many('hospital.appointment', 'patient_id', string='appointments')
   parent = fields.Char(string="parent")
   marital = fields.Selection([("maried","Maried"),("single","Single")], string='Marital Status')
   partner_name = fields.Char(string='Partner Name')

   @api.depends('appointments_ids')
   def _compute_appointment_count(self):
      for rec in self :
         rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])


   @api.constrains('dob')
   def _constraint_birth_date(self):
      for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
               raise ValidationError(_('Age cant be in negative value !'))

   @api.ondelete(at_uninstall=False)
   def check_if_appointment(self):
      for rec in self:
         if rec.appointments_ids:
            raise ValidationError(_('You can not delete patient with appointment already !'))

   @api.depends('dob')
   def _compute_age(self):
      for rec in self:
            if not rec.dob:
               continue
            else:
               rec.age = date.today().year - rec.dob.year
   
   @api.depends('age')
   def _compute_birth_day(self):
      for rec in self:
         rec.dob = date.today() - relativedelta.relativedelta(years=rec.age)

   def _search_age(self, operator, value):
   #    date_of_birth = date.today() - relativedelta.relativedelta(years=value)
   #    # start_of_date = date_of_birth.replace(day=1,month=1)
   #    # end_of_date = date_of_birth.replace(day=31,month=12)
   #    # return([('dob' ,'>=', start_of_date), ('dob' ,'<=', end_of_date)])
      date_of_birth = date.today() - relativedelta.relativedelta(years=value)
      return([('dob' ,'=', date_of_birth)])

   def action_in_progress(self):
      for rec in self:
            rec.state = 'in_progress'

   def action_done(self):
      for rec in self:
            rec.state = 'done'

   def action_cancel(self):
      for rec in self:
            rec.state = 'cancel'

   def action_draft(self):
      for rec in self:
            rec.state = 'draft'

   def action_test(self):
      print("............. test actoin_clicked ..............")
      return

   @api.model
   def create(self, vals):
      vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
      return super(HospitalPatient, self).create(vals)

   def write(self, vals):
      if not self.ref and not vals.get('ref') :
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
      return super(HospitalPatient, self).write(vals)

   def name_get(self):
      return [(rec.id,"[%s] %s" %(rec.ref, rec.name_id.name)) for rec in self]
      # return [(rec.id,(f"[{rec.ref}] {rec.name_id.name}")) for rec in self]
      
      # patient_list = []
      # for rec in self:
      #     name = rec.ref + ' ' + rec.name_id
      #     patient_list.append(rec.id, name)