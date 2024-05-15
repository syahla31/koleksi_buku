from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class transaksi(models.Model):
    _name = 'perpus.transaksi'
    _description = 'Model Transaksi Rental'

    tanggal_rental = fields.Date(string='Tanggal Rental', default=fields.Date.context_today)
    peminjam_id = fields.Many2one('perpus.member', string='Nama Peminjam', required=True)
    buku_ids = fields.Many2many('perpus.buku', string='Buku', required=True)
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam', required=True)
    tanggal_kembali = fields.Date(string='Tanggal Kembali',required=True)
    total_biaya = fields.Float(string='Total Biaya', compute='_compute_total_biaya')
    jumlah_hari = fields.Integer(string='Durasi Peminjaman', compute='_compute_jumlah_hari')

    @api.depends('tanggal_pinjam', 'tanggal_kembali')
    def _compute_jumlah_hari(self):
        for record in self:
            if record.tanggal_pinjam and record.tanggal_kembali:
                delta = relativedelta(record.tanggal_kembali, record.tanggal_pinjam)
                record.jumlah_hari = delta.days
            else:
                record.jumlah_hari = 0

    @api.depends('jumlah_hari')
    def _compute_total_biaya(self):
        for record in self:
            record.total_biaya = record.jumlah_hari * 1000