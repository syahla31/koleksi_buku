from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from datetime import date

class transaksi(models.Model):
    _name = 'perpus.transaksi'
    _description = 'Model Transaksi Rental'

    tanggal_rental = fields.Date(string='Tanggal Rental', default=fields.Date.context_today)
    peminjam_id = fields.Many2one(
        'perpus.member', 
        string='Nama Peminjam',
        domain=[('state','=', 'approved')], 
        required=True)
    buku_ids = fields.Many2many(
        'perpus.buku', 
        string='Buku', 
        domain=[('manajemenbuku_id.qty_tersedia', '>', 0)],
        required=True)
    tanggal_pinjam = fields.Date(string='Tanggal Pinjam', required=True)
    tanggal_kembali = fields.Date(string='Tanggal Kembali',required=True)
    total_biaya = fields.Float(string='Total Biaya', compute='_compute_total_biaya')
    jumlah_hari = fields.Integer(string='Durasi Peminjaman', compute='_compute_jumlah_hari')
    buku_names = fields.Char(string='Judul Buku', compute='_compute_buku_names')

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
    
    @api.depends('buku_ids')
    def _compute_buku_names(self):
        for record in self:
            record.buku_names = ', '.join(record.buku_ids.mapped('name'))
            
    @api.constrains('tanggal_pinjam', 'tanggal_kembali')
    def _check_tanggal_pinjam_kembali(self):
        for record in self:
            if record.tanggal_pinjam < date.today() or record.tanggal_kembali < date.today():
                raise ValidationError('Tanggal pinjam dan tanggal kembali tidak boleh kurang dari hari ini.')
            if record.tanggal_kembali < record.tanggal_pinjam:
                raise ValidationError('Tanggal kembali tidak boleh kurang dari tanggal pinjam.')

    @api.onchange('tanggal_pinjam', 'tanggal_kembali')
    def _onchange_tanggal(self):
        if self.tanggal_pinjam and self.tanggal_pinjam < date.today():
            self.tanggal_pinjam = date.today()
            return {
                'warning': {
                    'title': "Tanggal Tidak Valid",
                    'message': "Tanggal pinjam tidak boleh kurang dari hari ini."
                }
            }
        if self.tanggal_kembali and self.tanggal_kembali < date.today():
            self.tanggal_kembali = date.today()
            return {
                'warning': {
                    'title': "Tanggal Tidak Valid",
                    'message': "Tanggal kembali tidak boleh kurang dari hari ini."
                }
            }
    
    @api.model
    def create(self, vals):
        res = super(transaksi, self).create(vals)
        if 'buku_ids' in vals:
            for buku in res.buku_ids:
                manajemen_buku = self.env['perpus.manajemenbuku'].search([('name', '=', buku.id)], limit=1)
                if manajemen_buku and manajemen_buku.qty_tersedia > 0:
                    manajemen_buku.qty_tersedia -= 1
                else:
                    raise ValueError(_('Buku %s tidak tersedia untuk dipinjam.') % buku.name)
        return res

    def write(self, vals):
        for record in self:
            # Simpan buku_ids asli sebelum pembaruan
            original_buku_ids = set(record.buku_ids.ids)
            super(transaksi, record).write(vals)
            # Dapatkan buku_ids setelah pembaruan
            updated_buku_ids = set(record.buku_ids.ids)

            # Buku yang dihapus dari transaksi
            removed_buku_ids = original_buku_ids - updated_buku_ids
            # Buku yang ditambahkan ke transaksi
            added_buku_ids = updated_buku_ids - original_buku_ids

            # Menambah stok buku yang dihapus dari transaksi
            for buku_id in removed_buku_ids:
                manajemen_buku = self.env['perpus.manajemenbuku'].search([('name', '=', buku_id)], limit=1)
                if manajemen_buku:
                    manajemen_buku.qty_tersedia += 1

            # Mengurangi stok buku yang ditambahkan ke transaksi
            for buku_id in added_buku_ids:
                manajemen_buku = self.env['perpus.manajemenbuku'].search([('name', '=', buku_id)], limit=1)
                if manajemen_buku and manajemen_buku.qty_tersedia > 0:
                    manajemen_buku.qty_tersedia -= 1
                else:
                    raise ValueError(_('Buku %s tidak tersedia untuk dipinjam.') % manajemen_buku.name)

        return True
    
    def unlink(self):
        for record in self:
            for buku in record.buku_ids:
                manajemen_buku = self.env['perpus.manajemenbuku'].search([('name', '=', buku.id)], limit=1)
                if manajemen_buku:
                    manajemen_buku.qty_tersedia += 1
        return super(transaksi, self).unlink()