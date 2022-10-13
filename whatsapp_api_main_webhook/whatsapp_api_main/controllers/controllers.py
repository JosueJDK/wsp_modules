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
        # Get headers, data Request
        headers = request.httprequest.headers
        data = request.jsonrequest
        
        # Get ip of server
        ip_address = request.httprequest.environ['REMOTE_ADDR']

        # Get Values of request
        authorization = headers['Authorization'].split(" ")[1]
        data_base_name = data['db_name']
        user_name = data['user_name']
        
        # Search user_account
        account_user = data_users.search([('name', '=', user_name)])

        if account_user.token_verify == authorization:
            Response.status = '200'
        else:
            Response.status = '401'
        
        data_response = {
                'status' : Response.status,
                'token' : account_user.token,
                'url' : account_user.url
            }
            
        # Create registration of request
        new_request = {
            'name' : '',
            'db_name' : data_base_name,
            'ip_server' : ip_address,
            'status_code' : Response.status
        }
        create_request = data_request.create(new_request)
        # Create registration of messages
        new_message = {
            'name' : account_user.id,
            'id_request' : create_request.id,
            'messaging_product' : data['message']['messaging_product'],
            'recipient_type' : data['message']['recipient_type'],
            'recipient_id' : data['message']['to'],
            'status_code' : Response.status
        }
        data_message.create(new_message)

        return data_response