# -*- coding: utf-8 -*-
from odoo import fields, models


class TrafoQualityCheck(models.Model):
    _name = 'trafo.quality.check'
    _description = 'Trafo Quality Check'

    production_id = fields.Many2one(
        'trafo.production', string='Order Produksi', ondelete='cascade'
    )
    check_name = fields.Char(string='Item Pemeriksaan', required=True)
    result = fields.Selection([
        ('pass', 'Lulus'),
        ('fail', 'Gagal'),
    ], string='Hasil', default='pass')
    checked_by = fields.Many2one(
        'res.users', string='Diperiksa Oleh', default=lambda self: self.env.user
    )
    notes = fields.Text(string='Catatan')