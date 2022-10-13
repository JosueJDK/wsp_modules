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
        return kw
