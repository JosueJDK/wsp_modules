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

    def get_message_format_json(self):
        message = {
            "messaging_product": self.messaging_product,
            "recipient_type": self.recipient_type,
            "to": self.recipient_id,
            "type": "text",
            "text": {
                "preview_url": False, 
                "body": self.text_message
            }
        }
        return message

    def request_whatsapp_bussines_api(self):
        json_message = self.get_message_format_json()
        response_data = self.request_whatsapp_api_main(json_message)

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(response_data['result']['token']),
        }
        requests.post(f"{response_data['result']['url']}", headers=headers, json=response_data['result']['message'])

    def request_whatsapp_api_main(self, data):
        headers = {
            "Content-Type": "application/json",
            "Authorization" : "Bearer 30cca545-3838-48b2-80a7-9e43b1ae8ce4"
        }
        response = requests.post('http://154.12.228.77:8069/api/home', headers=headers, json=data)
        my_json = response.content.decode('utf8').replace("'",'"')
        response_data = json.loads(my_json)
        return response_data

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