# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo import exceptions

class WhatsAppRequests(models.Model):
    _name = 'whatsapp.api.main.requests'
    _description = 'Registro de solicitudes'
    _order = 'create_date desc'

    name = fields.Char(string="ID Requets", default="/",readonly=True)
    db_name = fields.Char(string="DataBase Name", require=True, readonly=True)
    ip_server = fields.Char(string="Direction IP of Servidor", require=True, readonly=True)
    type_request = fields.Char(string="Tipo de Solicitud!")
    status_code = fields.Selection(selection=[('200', 'Done'),('401', 'Unauthorized')], string='Code Status Request', default='401', readonly=True)

    def create(self, vals):
        self._cr.execute("""
            select	max(split_part(name,'/',2)::int)
                            from whatsapp_api_main_requests where name != '/'
        """)
        max_num = self._cr.fetchone()
        max_num = max_num[0]+1 if max_num[0] else 1
        rec_name = 'Solicitud RQT/'+str(max_num).zfill(3)
        vals['name'] = rec_name
        return super(WhatsAppRequests, self).create(vals)

    def unlink(self):
        raise exceptions.Warning('No puedes eliminar registros de solicitudes!')

class AccountsWABA(models.Model):
    _name = 'whatsapp.api.main.users'
    _description = 'Credenciales de WhatsApp Bussines Api Cloud'

    name = fields.Char(string="Name", require=True)
    token_verify = fields.Char(string="Token Requests", require=True)
    phone_number_id = fields.Char(string="Id phone number", require=True)
    token = fields.Char(string="Token WABA", requiere=True)
    url = fields.Char(string="URL complete", compute='_get_url')
    
    @api.depends('phone_number_id')
    def _get_url(self):
        self.url = f"https://graph.facebook.com/v14.0/{self.phone_number_id}/messages"


class WhatsAppMessages(models.Model):
    _name = 'whatsapp.api.main.messages'
    _description = 'Registro de Mensajes'
    _order = 'create_date desc'

    name = fields.Char(string="Name Message", default="/",readonly=True)
    id_request = fields.Many2one('whatsapp.api.main.requests', string="Id request", readonly=True)
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