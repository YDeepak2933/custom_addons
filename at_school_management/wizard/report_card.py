from odoo import models, fields

class ReportCardWizard(models.TransientModel):
    _name = 'report.card.wizard'
    _description = 'Report Card Wizard'

    student_id = fields.Many2one('school.student')
    academic_id = fields.Many2one('school.academic.year', required=True)
    
    def action_confirm(self):
        self.ensure_one()
        results = self.env['school.exam.result'].search([
            ('student_id', '=', self.student_id.id)
        ])
        data={
            "student_id":self.student_id,
            "data":[{"exam_id":r.exam_id,} for r in results]
        }
        return self.env.ref('at_school_management.action_report_card_pdf').report_action(self, data=data)
