from odoo import models, fields

class FeePaymentWizard(models.TransientModel):
    _name = 'fee.payment.wizard'
    _description = 'Fee Payment Wizard'

    student_id = fields.Many2one('school.student')
    academic_id = fields.Many2one('school.academic.year', required=True)
    
    def action_confirm(self):
        data = {
            'student_id': self.student_id.id if self.student_id else False,
            'academic_id': self.academic_id.id,
        }

        return self.env.ref('at_school_management.action_fee_xlsx').report_action(self, data=data)
    

