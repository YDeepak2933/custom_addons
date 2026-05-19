from odoo import models

class FeeXlsxReport(models.AbstractModel):
    _name = 'report.at_school_management.fee_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):

        sheet = workbook.add_worksheet('Fee Report')

        # Styles
        header_format = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'center'
        })

        normal_format = workbook.add_format({
            'border': 1
        })

        # Headers
        headers = ['Student', 'Total', 'Paid', 'Balance']

        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Domain filter
        domain = [('academic_id', '=', data['academic_id'])]

        if data.get('student_id'):
            domain.append(('student_id', '=', data['student_id']))

        fees = self.env['school.fee.payment'].search(domain)

        # Fill data
        row = 1
        for fee in fees:
            sheet.write(row, 0, fee.student_id.name or '', normal_format)
            sheet.write(row, 1, fee.total_amount or 0, normal_format)
            sheet.write(row, 2, fee.amount_paid or '', normal_format)
            sheet.write(row, 3, str(fee.balance_amount or ''), normal_format)
            row += 1