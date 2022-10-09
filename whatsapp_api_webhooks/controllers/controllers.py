# -*- coding: utf-8 -*-
from odoo import _,http
from odoo.http import request, Response

class WhatsappApiMain(http.Controller):
    @http.route('/api/webhooks', auth='public', type='json', csrf=False, website=False, methods=['GET', 'POST'])
    def index(self, **kw):

        # Get headers, data Request
        headers = request.httprequest.headers
        data = request.jsonrequest
        args = request.httprequest.args

        return args