from odoo import api, fields, models
from odoo.exceptions import UserError


class TrafoProduction(models.Model):
    _name = 'trafo.production'
    _description = 'Order Produksi Trafo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nomor Produksi', 
        required=True, 
        copy=False, 
        readonly=True, 
        default='New'
    )
    product_id = fields.Many2one(
        'product.product', 
        string='Produk Trafo', 
        required=True
    )
    capacity_kva = fields.Float(string='Kapasitas (kVA)', default=0.0)
    quantity = fields.Integer(string='Jumlah', default=1)
    responsible_id = fields.Many2one(
        'res.users', 
        string='Penanggung Jawab', 
        default=lambda self: self.env.user
    )
    
    start_date = fields.Datetime(string='Tanggal Mulai', readonly=True)
    end_date = fields.Datetime(string='Tanggal Selesai', readonly=True)
    
    unit_cost = fields.Float(string='Biaya Per Unit', default=0.0)
    
    total_cost = fields.Float(
        string='Total Biaya', 
        compute='_compute_total_cost', 
        store=True
    )
    
    quality_passed = fields.Boolean(
        string='Lolos QC', 
        compute='_compute_quality_passed', 
        store=True
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Dalam Produksi'),
        ('quality_check', 'Pemeriksaan QC'),
        ('done', 'Selesai'),
        ('cancel', 'Dibatalkan'),
    ], string='Status', default='draft', tracking=True)

    quality_check_ids = fields.One2many(
        'trafo.quality.check', 
        'production_id', 
        string='Pemeriksaan Kualitas'
    )
    
    notes = fields.Text(string='Catatan Tambahan')

    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = float(rec.quantity * rec.unit_cost) if rec.quantity and rec.unit_cost else 0.0

    @api.depends('quality_check_ids.result')
    def _compute_quality_passed(self):
        for rec in self:
            checks = rec.quality_check_ids
            if checks and all(check.result == 'pass' for check in checks):
                rec.quality_passed = True
            else:
                rec.quality_passed = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('trafo.production') or 'New'
        return super(TrafoProduction, self).create(vals)

    def action_start_production(self):
        for rec in self:
            rec.write({
                'state': 'in_progress',
                'start_date': fields.Datetime.now()
            })

    def action_send_to_qc(self):
        for rec in self:
            rec.state = 'quality_check'

    def action_done(self):
        for rec in self:
            if not rec.quality_passed:
                raise UserError('Produksi tidak dapat diselesaikan karena pemeriksaan QC belum lolos seluruhnya!')
            rec.write({
                'state': 'done',
                'end_date': fields.Datetime.now()
            })

    def action_cancel(self):
        for rec in self:
            if not rec.notes:
                raise UserError('Silakan tambahkan catatan sebelum membatalkan produksi.')
            rec.state = 'cancel'

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'draft'


class TrafoQualityCheck(models.Model):
    _name = 'trafo.quality.check'
    _description = 'Pemeriksaan Kualitas Trafo'

    production_id = fields.Many2one(
        'trafo.production', 
        string='Order Produksi', 
        ondelete='cascade'
    )
    check_name = fields.Char(string='Nama Pengujian', required=True)
    
    result = fields.Selection(
        selection=[
            ('pass', 'Lolos'),
            ('fail', 'Gagal'),
            ('pending', 'Pending')
        ], 
        string='Hasil', 
        default='pending'
    )
    checked_by = fields.Many2one(
        'res.users', 
        string='Diuji Oleh', 
        default=lambda self: self.env.user
    )
    notes = fields.Text(string='Catatan')