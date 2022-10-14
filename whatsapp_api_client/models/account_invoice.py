# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_link(self):
        for inv in self:
            base_url = inv.get_base_url()
            share_url = inv._get_share_url()
            url = base_url + share_url
            return url
    
    def action_send_whatsapp(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Send Message'),
                'res_model': 'whatsapp.send.message',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'account_move_id': self.id},
        }