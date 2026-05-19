from odoo import models, fields,api


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class Record'

    @api.depends('fee_structure_ids.amount')
    def _compute_amount(self):
        for record in self:
            record.amount = sum(line.amount for line in record.fee_structure_ids) if record.fee_structure_ids else 0

    name = fields.Char(string="Class Name", required=True)
    section = fields.Char(string="Section")
    grade = fields.Char(string="Grade")
    academic_id = fields.Many2one('school.academic.year', string="Academic Year")
    students = fields.One2many('school.student', 'class_id', string="Students")
    fee_structure_ids = fields.One2many('class.fee.structure', 'class_id', string="Fee Structure")
    amount = fields.Monetary(currency_field='currency_id',string="Total Fee", compute="_compute_amount", store=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )

class ClassFeeStructure(models.Model):
    _name = 'class.fee.structure'
    _description = 'Class Fee Structure'

    class_id = fields.Many2one('school.class', string="Class",ondelete='cascade')
    description = fields.Text(string='Description')
    amount = fields.Monetary(currency_field='currency_id',string='Amount')
    fee_type_id = fields.Many2one('school.fee.type', string="Fee Type", required=True)
    currency_id = fields.Many2one(
        'res.currency',
        related='class_id.currency_id',
        store=True
    )

    @api.onchange('fee_type_id')
    def _onchange_fee_type_id(self):
        if self.fee_type_id:
            self.description = self.fee_type_id.description
            self.amount = self.fee_type_id.amount