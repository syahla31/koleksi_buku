# addon/perpus/models/member.py

from odoo import models, fields, api

class Member(models.Model):
    _name = 'perpus.member'
    _description = 'Perpustakaan Member'

    name = fields.Char(string='Nama')
    no_identitas = fields.Char(string='No Identitas')
    jenis_identitas = fields.Selection([
        ('ktp', 'KTP'),
        ('sim', 'SIM'),
        ('passport', 'Pasport')
    ], string='Jenis Identitas', default='ktp')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_approval', 'Waiting Approval'), # Tambahkan opsi ini
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='draft')

    def action_send_approval(self):
        self.state = 'waiting_approval'

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'