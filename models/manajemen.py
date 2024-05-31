from odoo import models, fields, api

class ManajemenBuku(models.Model):
    _name = 'perpus.manajemenbuku'
    _description = 'Model Manajemen Buku'

    name = fields.Many2one('perpus.buku', string='Buku', required=True, domain=lambda self: self._get_buku_domain())
    serial_number = fields.Char(string='Serial Number', required=True)
    qty_tersedia = fields.Integer(string='Qty Tersedia', default=1)

    @api.model
    def _get_buku_domain(self):
        # Mendapatkan daftar ID buku yang sudah terdaftar di Manajemen Buku
        manajemen_buku_ids = self.search([]).mapped('name.id')
        # Mengembalikan domain untuk field 'name'
        return [('id', 'not in', manajemen_buku_ids)]

    # @api.onchange('name')
    # def _onchange_name(self):
    #     if self.name:
    #         self.serial_number = self.name.serial_number
