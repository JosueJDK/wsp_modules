# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, sql_db
from odoo.exceptions import UserError, ValidationError
import requests
import json
import re
import time

class Partner(models.Model):
    """Inherit Partner."""
    _inherit = "res.partner"

    chat_id = fields.Char(string='ChatID')
        
    def action_send_whatsapp(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.send.message',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.id},
    }