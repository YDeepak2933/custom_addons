from odoo import models, fields


class ExamResult(models.Model):
    _name = 'school.exam.result'
    _description = 'Exam Result'

    student_id = fields.Many2one('school.student', string="Student")
    exam_id = fields.Many2one('school.exam', string="Exam",ondelete='cascade')
    marks_obtained = fields.Integer(string="Marks Obtained")
    grade = fields.Char(string="Grade")
    status = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string="Status")
