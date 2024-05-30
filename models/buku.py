from odoo import api, fields, models
from odoo.tools.translate import _

class buku(models.Model):
    _name = 'perpus.buku'
    _description = 'Buku'
    
    name = fields.Char(string='Judul Buku', required=True)
    kategori = fields.Selection([
        ('umum', 'Umum'),
        ('it', 'IT'),
        ('kesehatan', 'Kesehatan'),
        ('politik', 'Politik')
    ], string='Kategori Buku', required=True)
    tgl_terbit = fields.Date(string='Tangal Terbit', required=True)
    penulis = fields.Many2many(comodel_name='res.partner', string='Penulis Buku', required=True)
    kode = fields.Char(string='Kode ISBN', required=True)
    manajemenbuku_id = fields.One2many('perpus.manajemenbuku', 'name', string='Manajemen Buku')
    peminjaman_ids = fields.One2many('perpus.transaksi', 'buku_ids', string='Peminjaman')
    buku_penulis_ids = fields.Many2many('perpus.buku', string='Buku Penulis', compute='_compute_buku_penulis_ids')

    @api.depends('penulis')
    def _compute_buku_penulis_ids(self):
        for buku in self:
            buku_penulis_ids = self.env['perpus.buku'].search([('penulis', 'in', buku.penulis.ids)])
            buku.buku_penulis_ids = buku_penulis_ids

    def action_view_buku_penulis(self):
        buku_penulis_ids = self.mapped('buku_penulis_ids').ids
        penulis_names = ', '.join(self.penulis.mapped('name'))
        return {
            'name': _('Penulis: %s') % penulis_names,
            'view_mode': 'tree,form',
            'res_model': 'perpus.buku',
            'domain': [('id', 'in', buku_penulis_ids)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        
    def action_view_peminjaman(self):
        transaksi_ids = self.env['perpus.transaksi'].search([('buku_ids', 'in', self.ids)])
        unique_judul_buku = transaksi_ids.mapped('buku_ids.name')
        domain = [('buku_ids.name', 'in', unique_judul_buku)]

        def _name_create(name, context):
            judul_buku = ', '.join(unique_judul_buku)
            return _('Peminjaman Buku: %s') % judul_buku

        return {
            'name': _name_create('Peminjaman Buku', self._context),
            'view_mode': 'tree,form',
            'res_model': 'perpus.transaksi',
            'domain': domain,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
