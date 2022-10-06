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
            data_response = {
                'status' : Response.status,
                'phone_number_id' : account_user.phone_number_id,
                'token' : account_user.token,
                'url' : account_user.url,
                'message' : data['message'],
            }
            self._cr.execute("""
                select	max(split_part(name,'/',2)::int)
                                from whatsapp_api_main_requests where name != '/'
            """)
            max_num = self._cr.fetchone()
            max_num = max_num[0]+1 if max_num[0] else 1
            rec_name = 'RQT/'+str(max_num).zfill(3)
            # Create registration of request
            new_request = {
                'name' : rec_name,
                'db_name' : data_base_name,
                'ip_server' : ip_address,
                'status_code' : Response.status
            }
            data_request.create(new_request)
            # Create registration of messages
            # new_message = {
            #     'name' : account_user.id,
            #     'id_request' : create_request.id,
            #     'messaging_product' : data['message']['messaging_product'],
            #     'recipient_type' : data['message']['recipient_type'],
            #     'recipient_id' : data['message']['to'],
            #     'status_code' : Response.status
            # }
            # data_message.create(new_message)
            return data_response
        else:
            Response.status = '401'
            # Create registration of request
            new_request = {
                'db_name' : data_base_name,
                'ip_server' : ip_address,
                'status_code' : Response.status
            }
            data_request.create(new_request)
            # Create registration of messages
            # new_message = {
            #     'name' : account_user.id,
            #     'id_request' : create_request.id,
            #     'messaging_product' : data['message']['messaging_product'],
            #     'recipient_type' : data['message']['recipient_type'],
            #     'recipient_id' : data['message']['to'],
            #     'status_code' : Response.status
            # }
            # data_message.create(new_message)
            return Response.status


#     @http.route('/whatsapp_api_main/whatsapp_api_main/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('whatsapp_api_main.listing', {
#             'root': '/whatsapp_api_main/whatsapp_api_main',
#             'objects': http.request.env['whatsapp_api_main.whatsapp_api_main'].search([]),
#         })

#     @http.route('/whatsapp_api_main/whatsapp_api_main/objects/<model("whatsapp_api_main.whatsapp_api_main"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('whatsapp_api_main.object', {
#             'object': obj
#         })
