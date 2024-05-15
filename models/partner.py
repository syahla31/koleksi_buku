from odoo import models, fields, api, _

class Partner(models.Model):
    _inherit = 'res.partner'

    buku_ids = fields.Many2many('perpus.buku', 'penulis', 'buku_ids', string='Buku')

    def action_view_buku_penulis(self):
        action = self.env.ref('perpus.action_master_buku').read()[0]
        action['context'] = {'search_default_penulis': self.id}
        return action