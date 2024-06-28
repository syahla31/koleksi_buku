from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class WizardReport(models.TransientModel):
    _name = 'wizard.report'
    _description = 'Wizard for Rental Report'

    show_all_date = fields.Boolean(string='Show All Dates', default=False)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def print_report_pdf(self):
        domain = []
        if not self.show_all_date:
            if not self.start_date or not self.end_date:
                raise ValidationError("Please provide both start and end dates.")
            domain = [
                ('tanggal_rental', '>=', self.start_date),
                ('tanggal_rental', '<=', self.end_date)
            ]

        transactions = self.env['perpus.transaksi'].search(domain)
        res_company = self.env.company

        data = {
            'ids': transactions.ids,
            'model': 'perpus.transaksi',
            'form': {
                'show_all_date': self.show_all_date,
                'start_date': self.start_date,
                'end_date': self.end_date,
            },
            'transactions': transactions.read(),
            'currency': res_company.currency_id
        }

        # Tambahkan logging untuk debug
        _logger.info("Data yang dikirim ke template: %s", data)
        return self.env.ref('koleksi_buku.action_report_rental_transactions').report_action(self)
    
    def get_transactions(self):
        domain = []
        if not self.show_all_date:
            domain = [
                ('tanggal_rental', '>=', self.start_date),
                ('tanggal_rental', '<=', self.end_date)
            ]
        return self.env['perpus.transaksi'].search(domain)
