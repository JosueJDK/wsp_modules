# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests, json

class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.message.wizard'

    partner_id = fields.Many2one('res.partner')
    cod_country = fields.Char(required=True)
    mobile = fields.Char(required=True)
    message = fields.Text(required=True)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.mobile = self.partner_id.mobile
    
    def send_message_text(self, message, recipient_id, preview_url=False):
        message_json = {
            "messaging_product": "whatsapp",
            "recipient_type": 'individual',
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        config_wsp = self.env['res.config.settings'].search([])
        for rec in config_wsp:
            user_name = rec.user_name
            verify_token = rec.verify_token
        data = {
                "db_name" : "db_prueba",
                "user_name" : user_name,
                "message" :  message_json
            }
        response_data = self.request_whatsapp_api_main(data, verify_token)
        if response_data[0] == True:
            response_data = response_data[1]
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(response_data['result']['token']),
            }
            requests.post(f"{response_data['result']['url']}", headers=headers, json=response_data['result']['message'])
            

    def request_whatsapp_api_main(self, data, verify_token):
        headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {verify_token}"
        }
        response = requests.post('http://192.168.2.20:8069/api/home', headers=headers, json=data)
        my_json = response.content.decode('utf8').replace("'",'"')
        response_data = json.loads(my_json)
        if response.status_code == 200:
            return True, response_data
        else: 
            return False, response_data
        print(response_data)
        
    
    def send_message(self):
        if self.message and self.mobile:
            toSend = self.cod_country + self.mobile
            response = self.send_message_text(self.message, toSend)
            print(response)

