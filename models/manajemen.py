from odoo import models, fields, api, _

class ManajemenBuku(models.Model):
    _name = 'perpus.manajemenbuku'
    _description = 'Model Manajemen Buku'

    name = fields.Many2one('perpus.buku', string='Buku', required=True)
    serial_number = fields.Char(string='Serial Number', required=True)
    # lokasi_rak = fields.Char(string='Lokasi Rak', required=True)
    qty_tersedia = fields.Integer(string='Qty Tersedia', default=1)
    stok = fields.Integer(string='Stok Buku Awal')
    
    #qty bersedia akan mengurang setiap ada peminjaman buku dan pengurangan dari stok buku awal. dan jika qty tersedia 0 maka buku tidak dapat dipinjam.
    
    
    