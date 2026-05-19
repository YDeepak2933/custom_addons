from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Parent(models.Model):
    _name = 'school.parent'
    _description = 'Parent/Guardian'

    name = fields.Char(string="Full Name", required=True)
    contact_no = fields.Char(string="Contact No", required=True)
    email = fields.Char(string="Email")
    occupation = fields.Char(string="Occupation")
    student_id = fields.Many2one('school.student', string="Student",ondelete='cascade')
    relation = fields.Selection([
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Guardian', 'Guardian')
    ], string="Relation", required=True)


    @api.constrains('contact_no')
    def _check_mobile_number(self):
        for record in self:
            if record.contact_no:
                pattern = r'^\+?\d{10}$'
                if not re.match(pattern, record.contact_no):
                    raise ValidationError("Invalid mobile number! It should be 10 digit.")


    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(pattern, record.email):
                    raise ValidationError("Invalid email format!")