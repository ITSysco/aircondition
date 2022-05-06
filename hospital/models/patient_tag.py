# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PatientTag(models.Model):
   _name = 'patient.tag'
   _description = 'Patient Tag'
   _rec_name = 'name'

   name = fields.Char(string='Name', required=True)
   active = fields.Boolean(string='Active', default=True)
   color = fields.Float(string='Color', copy=False)
   color_2 = fields.Char(string='Char Color', copy=False)
   Patients_ids = fields.Many2many('hospital.patient', 'patient_tag_ref', 'tag_id_name','patient_id_name' ,
                              string="Patients")
   sequence = fields.Integer(string='Sequence')

   api.returns('self', lambda value : value.id)
   def copy(self, default=None):
      if default is None:
         default = {}
      if not default.get('name'):
         default ['name'] = _("%s (copy)", self.name)
         default ['sequence'] = self.sequence + 1
      return super(PatientTag, self).copy(default)

   _sql_constraints = [
      ('kode_uniq_tag', 'unique(name, active)', 'Name Must Be Unique !'),
      ('check_size_sequence', 'CHECK (sequence > 0)', 'Sequence Must Be Greater Than Zero !')
   ]