from odoo import models, fields


class SchoolAcademicYear(models.Model):
    _name = 'school.academic.year'
    _description = 'School Academic Year'

    name = fields.Char(string="Year Name", required=True)
