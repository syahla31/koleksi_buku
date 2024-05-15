from odoo import models, fields, api, _

class ManajemenBuku(models.Model):
    _name = 'perpus.manajemenbuku'
    _description = 'Model Manajemen Buku'

    name = fields.Many2one('perpus.buku', string='Buku', required=True)
    serial_number = fields.Char(string='Serial Number', required=True)
    lokasi_rak = fields.Char(string='Lokasi Rak', required=True)
    qty_tersedia = fields.Integer(string='Qty Tersedia', default=1)