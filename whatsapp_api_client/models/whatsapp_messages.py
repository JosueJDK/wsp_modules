# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions

class WhatsAppMessages(models.Model):
    _name = 'whatsapp.api.client.messages'
    _description = 'Registro de Mensajes'
    _order = 'create_date desc'

    name = fields.Char(string="Name Message", default="/",readonly=True)
    partner_id = fields.Many2one('res.partner', string='Contact', require=True)
    messaging_product = fields.Char(string="Meta Service", default="whatsapp", readonly=True)
    recipient_type = fields.Char(string="Type of recipient", default="individual", readonly=True)
    recipient_id = fields.Char(string="Number of recipient", readonly=True)
    status_code = fields.Selection(selection=[('200', 'Done'),('401', 'Unauthorized'), ('err', 'Error')], string='Code Status Request', default='err', readonly=True)
    type_message = fields.Char(string="Type of message send", readonly=True)
    text_message = fields.Char(string="Data of message", readonly=True)
    link_file = fields.Char(string="URL of the File", readonly=True)
    filename = fields.Char(string="Name of the file", readonly=True)

    def create(self, vals):
        self._cr.execute("""
            select	max(split_part(name,'/',2)::int)
                            from whatsapp_api_client_messages where name != '/'
        """)
        max_num = self._cr.fetchone()
        max_num = max_num[0]+1 if max_num[0] else 1
        rec_name = 'Message MSG/'+str(max_num).zfill(3)
        vals['name'] = rec_name
        if vals['status_code'] != '200' and vals['status_code'] != '401':
            vals['status_code'] = 'err'
        return super(WhatsAppMessages, self).create(vals)


    def unlink(self):
        raise exceptions.Warning('No puedes eliminar registros de Mensajes!')

class WhatsAppMessagesTemplate(models.Model):
    _name = 'whatsapp.api.client.messages.templates'
    _description = 'Registro de Templates Mensajes'

    name = fields.Char(string="Name Message", required=True)