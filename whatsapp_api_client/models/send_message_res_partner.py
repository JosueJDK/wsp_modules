# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SendMessagesWhatsApp(models.Model):
    _inherit = 'res.partner'

    def action_send_whatsapp(self):
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'whatsapp.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.id}
        }

    