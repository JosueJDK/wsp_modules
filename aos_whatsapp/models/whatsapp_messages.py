# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import json  

class WhatsAppMessages(models.Model):
    _name = 'whatsapp.api.client.messages'
    _description = 'Registro de Mensajes'

    messaging_product = fields.Char(string="Meta Service", default="whatsapp")
    recipient_type = fields.Char(string="Type of recipient", default="individual")
    recipient_id = fields.Char(string="Number of recipient")
    text_message = fields.Char(string="Data of message")
    status_code = fields.Char(string="Code Status Request")
    
class WhatsAppMessagesLine(models.Model):
    _name = 'whatsapp.api.client.messages.line'
    _description = 'Registro del contenido de Mensajes'

    message_id = fields.Many2one('whatsapp.api.client.messages', string="Id Message")
    type_message = fields.Char(string="Type of message send")
    text_message = fields.Char(string="Data of message")
    preview_url = fields.Boolean('URL preview', default=True)
    link_file = fields.Char(string="URL of the File")
    caption = fields.Char(string="Captio of message(Only Type Image or Video)")
    filename = fields.Char(string="Name of the file(Only document)")

    
class WhatsAppMessagesLine(models.Model):
    _name = 'whatsapp.api.client.template'
    _description = 'Registro de Templates en Message'