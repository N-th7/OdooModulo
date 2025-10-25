from odoo import models
from datetime import date

class InternetServiceCut(models.Model):
    _inherit = 'internet.client'

    def _cron_check_clients_for_cut(self):
        clients = self.search([])
        for client in clients:
            if client.deuda_meses >= 2 and client.status != 'cortado':
                client.status = 'cortado'
