# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions

class WhatsAppMessages(models.Model):
    _name = 'whatsapp.api.main.messages'
    _description = 'Registro de Mensajes'
    _order = 'create_date desc'

    name = fields.Char(string="Name Message", default="/",readonly=True)
    messaging_product = fields.Char(string="Meta Service", default="whatsapp", readonly=True)
    recipient_type = fields.Char(string="Type of recipient", default="individual", readonly=True)
    recipient_id = fields.Char(string="Number of recipient", readonly=True)
    status_code = fields.Selection(selection=[('200', 'Done'),('401', 'Unauthorized'), ('err', 'Error')], string='Code Status Request', default='err', readonly=True)

    def create(self, vals):
        self._cr.execute("""
            select	max(split_part(name,'/',2)::int)
                            from whatsapp_api_main_messages where name != '/'
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

class WhatsAppMessagesLine(models.Model):
    _name = 'whatsapp.api.main.messages.line'
    _description = 'Registro del contenido de Mensajes'
    _order = 'create_date desc'

    message_id = fields.Many2one('whatsapp.api.main.messages', string="Id Message", readonly=True)
    type_message = fields.Char(string="Type of message send", readonly=True)
    type_message_body = fields.Char(string="Type of message body", readonly=True)
    text_message = fields.Char(string="Data of message", readonly=True)
    type_message_header = fields.Char(string="Type of message header", readonly=True)
    link_file = fields.Char(string="URL of the File", readonly=True)
    filename = fields.Char(string="Name of the file(Only document)", readonly=True)

    def unlink(self):
        raise exceptions.Warning('No puedes eliminar registros de Mensajes!')