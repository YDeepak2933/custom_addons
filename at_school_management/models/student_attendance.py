from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'
    _order = 'date desc, id desc'
    _rec_name = 'display_name'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    class_id = fields.Many2one('school.class', string='Class', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], default='draft', string='Status')
    
    line_ids = fields.One2many('student.attendance.line', 'attendance_id', string='Attendance Lines')
    
    total_students = fields.Integer(compute='_compute_stats', string='Total')
    total_present = fields.Integer(compute='_compute_stats', string='Present')
    total_absent = fields.Integer(compute='_compute_stats', string='Absent')
    
    display_name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        ('unique_class_date', 'unique(class_id, date)', 
         'Attendance for this class and date already exists!')
    ]

    @api.depends('class_id', 'date')
    def _compute_display_name(self):
        for rec in self:
            if rec.class_id and rec.date:
                rec.display_name = f"{rec.class_id.name} - {rec.date}"
            else:
                rec.display_name = "New Attendance"

    @api.depends('line_ids.is_present')
    def _compute_stats(self):
        for rec in self:
            rec.total_students = len(rec.line_ids)
            rec.total_present = len(rec.line_ids.filtered(lambda l: l.is_present))
            rec.total_absent = rec.total_students - rec.total_present

    @api.onchange('class_id', 'date')
    def _onchange_class_id(self):
        if self.class_id and self.date:
            # Clear existing lines first
            self.line_ids = [(5, 0, 0)]
            # Get all students in this class
            students = self.env['school.student'].search([
                ('class_id', '=', self.class_id.id),
                # ('active', '=', True)
            ])
            lines = []
            for student in students:
                lines.append((0, 0, {
                    'student_id': student.id,
                    'is_present': True,  # Default to present
                }))
            self.line_ids = lines

    def action_done(self):
        self.state = 'done'
        return True

    def action_draft(self):
        self.state = 'draft'
        return True

class StudentAttendanceLine(models.Model):
    _name = 'student.attendance.line'
    _description = 'Student Attendance Line'
    _order = 'student_id'

    attendance_id = fields.Many2one('student.attendance', string='Sheet', 
                               required=True, ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True)
    is_present = fields.Boolean(string='Present', default=True)
    remarks = fields.Char(string='Remarks')
    
    # Related fields for easy filtering
    date = fields.Date(related='attendance_id.date', store=True)
    class_id = fields.Many2one(related='attendance_id.class_id', store=True)