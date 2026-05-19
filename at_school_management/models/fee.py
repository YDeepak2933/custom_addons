from odoo import models, fields, api

class FeePayment(models.Model):
    _name = 'school.fee.payment'
    _description = 'Fee Payment'
    _order = 'date desc'
    

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('school.fee.payment') or 'New'
        return super().create(vals_list)

    name = fields.Char(required=True,default="New",copy=False)
    student_id = fields.Many2one('school.student', string="Student", required=True)
    academic_id = fields.Many2one('school.academic.year', string="Academic Year", required=True)
    fee_line_ids = fields.One2many('school.fee.payment.line', 'fee_payment_id',string="Fee Type", required=True)
    fee_collection_ids = fields.One2many('school.fee.payment.collection', 'fee_payment_id',string="Payment Collection")
    amount_paid = fields.Monetary(currency_field='currency_id',string="Paid",compute="_compute_total_amount", store=True)
    total_amount = fields.Monetary(currency_field='currency_id',string="Total", compute="_compute_total_amount", store=True)
    balance_amount = fields.Monetary(currency_field='currency_id',string="Balance", compute="_compute_balance_amount", store=True)
    note = fields.Text(string="Remarks / Description")
    date = fields.Date(string="Date", required=True, default=fields.Date.today)
    class_id = fields.Many2one('school.class', string="Class", required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    user_id = fields.Many2one(comodel_name='res.users', string="User", readonly=True,
    default=lambda self: self.env.user
    )

    
    @api.depends('fee_line_ids.amount','fee_collection_ids.paid')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.amount for line in record.fee_line_ids) if record.fee_line_ids else 0
            record.amount_paid = sum(line.paid for line in record.fee_collection_ids) if record.fee_collection_ids else 0
            record.balance_amount =  (record.total_amount - record.amount_paid)

    @api.depends('total_amount', 'amount_paid')
    def _compute_balance_amount(self):
        for record in self:
            record.balance_amount = record.total_amount - record.amount_paid

    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            self.class_id = self.student_id.class_id


    @api.onchange('class_id')
    def _onchange_class(self):
        if not self.class_id:
            self.fee_line_ids = [(5, 0, 0)]  # clear all
            return

        lines = []

        for fee in self.class_id.fee_structure_ids:
            lines.append((0, 0, {
                'fee_type_id': fee.fee_type_id.id,
                'amount': fee.amount,
                'description': fee.description,
            }))

        self.fee_line_ids = [(5, 0, 0)] + lines


    class FeePaymentLine(models.Model):
        _name = 'school.fee.payment.line'
        _description = 'Fee Payment Line'

        fee_payment_id = fields.Many2one('school.fee.payment', string="Fee Id", required=True,ondelete='cascade')
        description = fields.Text(string='Description')
        amount = fields.Monetary(currency_field='currency_id',string='Amount')
        fee_type_id = fields.Many2one('school.fee.type', string="Fee Type", required=True)
        currency_id = fields.Many2one(
            'res.currency',
            related='fee_payment_id.currency_id',
            store=True
        )

        @api.onchange('fee_type_id')
        def _onchange_fee_type_id(self):
            if self.fee_type_id:
                self.description = self.fee_type_id.description
                self.amount = self.fee_type_id.amount


    class FeePaymentCollection(models.Model):
        _name = 'school.fee.payment.collection'
        _description = 'Fee Payment Collection'

        fee_payment_id = fields.Many2one('school.fee.payment', string="Fee Id",ondelete='cascade')
        description = fields.Text(string='Remarks')
        paid = fields.Monetary(currency_field='currency_id',string='Paid')
        date = fields.Date(string="Date", required=True, default=fields.Date.today)
        payment_mode = fields.Selection(
            [('cash', 'Cash'), ('online', 'Online'), ('cheque', 'Cheque')],
            string="Payment Mode", required=True
        )
        currency_id = fields.Many2one(
            'res.currency',
            related='fee_payment_id.currency_id',
            store=True
        )

        def action_fee_receipt_report_pdf(self):
            self.ensure_one()
            return self.env.ref('at_school_management.action_fee_receipt_report').report_action(self)