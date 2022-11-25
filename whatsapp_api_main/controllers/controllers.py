# -*- coding: utf-8 -*-
from odoo import _,http
from odoo.http import request, Response

class WhatsappApiMain(http.Controller):
    @http.route('/api/home', auth='public', type='json', csrf=False, website=False, methods=['GET', 'POST'])
    def index(self, **kw):
        # Table of Data Base
        data_request = request.env['whatsapp.api.main.requests'].sudo()
        data_users = request.env['whatsapp.api.main.users'].sudo()
        data_message = request.env['whatsapp.api.main.messages'].sudo()

        headers = request.httprequest.headers
        data = request.jsonrequest

        # Get ip of server
        ip_address = request.httprequest.environ['REMOTE_ADDR']

        # Get Values of request
        authorization = headers['Authorization'].split(" ")[1]
        data_base_name = data['db_name']
        user_name = data['user_name']

        verification_status = self.check_user_authenticate(data, headers, data_users)

        if verification_status:
            if data['type'] == 'authorization':
                Response.status = '200'
                data_response = {
                    'status' : Response.status,
                    'token' : verification_status.token,
                    'url' : verification_status.url
                }
            elif data['type'] == 'save_message':
                Response.status = '200'
                data_response = {
                    'Ok' : data['message_data']
                }

            elif data['type'] == 'SendMessageWhatsapp':                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(verification_status.token),
                }
                res =  requests.post(f"{verification_status.url}", headers=headers, json=data['message_json'])
                Response.status = res.status_code
                
            else:
                Response.status = '401'
                data['type'] = 'Desconocido!'
                data_response = {
                    "Error" : data['type']
                }
        else:
            Response.status = '401'
            data_response = {
                "Error" : Response.status
            }

        # Create registration of request
        new_request = {
            'name' : '',
            'db_name' : data_base_name,
            'ip_server' : ip_address,
            'type_request' : data['type'],
            'status_code' : Response.status
        }
        create_request = data_request.create(new_request)
        if data['type'] == 'save_message':
            # Create registration of messages
            new_message = {
                'name' : '',
                'id_request' : create_request.id,
                'messaging_product' : data['message_data']['messaging_product'],
                'recipient_type' : data['message_data']['recipient_type'],
                'recipient_id' : data['message_data']['recipient_id'],
                'status_code' : str(data['message_data']['status_code']),
                'type_message' : data['message_data']['type_message'],
                'text_message' : data['message_data']['text_message'],
                'link_file' : data['message_data']['link_file'],
                'filename' : data['message_data']['filename'],
            }
            data_message.create(new_message)
        return data_response
    
    def check_user_authenticate(self, data, headers, data_users):
        authorization = headers['Authorization'].split(" ")[1]
        data_base_name = data['db_name']
        user_name = data['user_name']
        # Search user_account
        account_user = data_users.search([('name', '=', user_name)])

        if account_user.token_verify == authorization and account_user.state_service == True:
            return account_user
        else:
            return False