from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string="Full Name", required=True,store=True)
    first_name = fields.Char(string="First Name", required=True)
    middle_name = fields.Char(string="Middle Name")
    last_name = fields.Char(string="Last Name", required=True)
    admission_no = fields.Char(string="Admission No", required=True, unique=True)
    dob = fields.Date(string="Date of Birth", required=True,)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", required=True,)
    medical_history = fields.Text(string="Medical History")
    parent_id = fields.One2many('school.parent','student_id',string="Parent/Guardian")
    class_id = fields.Many2one('school.class', string="Class", required=True,ondelete='cascade')
    document_ids = fields.One2many('school.student.document', 'student_id', string="Documents")
    blood_group = fields.Selection([
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B-', 'B-'),
        ('B+', 'B+'),
        ('AB-', 'AB-'),
        ('AB+', 'AB+')
    ], string="Blood group", required=True,)
    is_student = fields.Boolean(string="Is Student", default=True)
    roll_no = fields.Char(string="Roll No", unique=True, required=True)
    house_address = fields.Text(string="Home Address", required=True)
    doj = fields.Date(string="Date of Admission", required=True)
    trackskill = fields.Text(string="Track Skills")
    user_id = fields.Many2one(comodel_name='res.users', string="User", readonly=True,
    default=lambda self: self.env.user
    )
    email = fields.Char(string="Email")
    # 👇 New field for uploading and storing student image
    image_1920 = fields.Image(string="Student Photo", max_width=1920, max_height=1920, store=True)


    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email:
                pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(pattern, record.email):
                    raise ValidationError("Invalid email format!")
                    
    @api.onchange('first_name','middle_name','last_name')
    def _onchange_name(self):
        if self.first_name:
            self.name = " ".join([self.first_name,self.middle_name or '',self.last_name or ''])
