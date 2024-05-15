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
        return {
            'name': _('Peminjaman Buku'),
            'view_mode': 'tree,form',
            'res_model': 'perpus.transaksi',
            'domain': [('buku_ids', '=', self.id)],
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
    
