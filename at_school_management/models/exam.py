from odoo import models, fields

class Exam(models.Model):
    _name = 'school.exam'
    _description = 'Exam Record'

    name = fields.Char(string="Exam Name", required=True)
    class_id = fields.Many2one('school.class', string="Class")
    subject_id = fields.Many2one('school.subject', string="Subject")
    exam_datetime = fields.Datetime(string="Start Date and Time")
    exam_end_datetime = fields.Datetime(string="End Date and Time")
    max_marks = fields.Integer(string="Max Marks")
    passing_marks = fields.Integer(string="Passing Marks")
    exam_result_ids = fields.One2many('school.exam.result', 'exam_id',string="Result")
    academic_id = fields.Many2one('school.academic.year', string="Academic Year")

    def action_create_exam_result(self):
        self.ensure_one()
        if not self.class_id:
            self.exam_result_ids = [(5, 0, 0)]  # clear all
            return

        lines = []

        students = self.env['school.student'].search([
            ('class_id', '=', self.class_id.id)
        ])
        for s in students:
            lines.append((0, 0, {
                'student_id': s.id,
            }))

        self.exam_result_ids = [(5, 0, 0)] + lines