# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions

class WhatsAppRequests(models.Model):
    _name = 'whatsapp.api.main.requests'
    _description = 'Registro de solicitudes'
    _order = 'create_date desc'

    name = fields.Char(string="ID SOLICITUd", default="/",readonly=True)
    db_name = fields.Char(string="Nom. Base Datos", require=True, readonly=True)
    ip_server = fields.Char(string="Direccion IP del Servidor", require=True, readonly=True)
    type_request = fields.Char(string="Tipo de Solicitud!")
    status_code = fields.Selection(selection=[('200', 'Done'),('401', 'Unauthorized')], string='Codigo de estado', default='401', readonly=True)

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

    name = fields.Char(string="Nombre Usuario", require=True)
    state_service = fields.Boolean(string="Estado!")
    token_verify = fields.Char(string="Clave Acceso Usuario", require=True)
    phone_number_id = fields.Char(string="Id numero Telefono", require=True)
    token = fields.Char(string="Token WhatsApp", requiere=True)
    url = fields.Char(string="URL BASE", compute='_get_url')
    
    @api.depends('phone_number_id')
    def _get_url(self):
        self.url = f"https://graph.facebook.com/v14.0/{self.phone_number_id}/messages"


class WhatsAppMessages(models.Model):
    _name = 'whatsapp.api.main.messages'
    _description = 'Registro de Mensajes'
    _order = 'create_date desc'

    name = fields.Char(string="Nom. Mensaje", default="/",readonly=True)
    id_request = fields.Many2one('whatsapp.api.main.requests', string="Id Solicitud", readonly=True)
    messaging_product = fields.Char(string="Tipo de Servicio", default="whatsapp", readonly=True)
    recipient_type = fields.Char(string="Tipo de Receptor", default="individual", readonly=True)
    recipient_id = fields.Char(string="Numero Receptor", readonly=True)
    status_code = fields.Selection(selection=[('200', 'Done'), ('err', 'Error')], string='Codigo Estado', default='err', readonly=True)
    type_message = fields.Char(string="Tipo de Mensaje", readonly=True)
    text_message = fields.Char(string="Contenido del Mensaje", readonly=True)
    link_file = fields.Char(string="URL del archivo", readonly=True)
    filename = fields.Char(string="Nombre del rchivo(Solo documentos)", readonly=True)

    def create(self, vals):
        self._cr.execute("""
            select	max(split_part(name,'/',2)::int)
                            from whatsapp_api_main_messages where name != '/'
        """)
        max_num = self._cr.fetchone()
        max_num = max_num[0]+1 if max_num[0] else 1
        rec_name = 'Message MSG/'+str(max_num).zfill(3)
        vals['name'] = rec_name
        if vals['status_code'] != '200':
            vals['status_code'] = 'err'
        return super(WhatsAppMessages, self).create(vals)


    def unlink(self):
        raise exceptions.Warning('No puedes eliminar registros de Mensajes!')