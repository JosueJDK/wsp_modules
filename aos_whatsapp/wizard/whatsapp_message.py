# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import base64, requests, json

class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.send.message'
    _description = "Whatsapp Message"

    partner_id = fields.Many2one('res.partner', string='Contact')
    subject = fields.Char('Subject')
    message = fields.Text()
    model = fields.Char('Object')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'whatsapp_send_message_ir_attachments_rel',
        'wizard_id', 'attachment_id', 'Attachments')
    number_phone = fields.Char(string='Phone Address')
    link_document = fields.Char(string="Link PDF")
    file_document = fields.Char(string="PDF name")
    template_id = fields.Many2one('mail.template', 'Use template', index=True,) 

    def whatsapp_message_post(self):
        print("Message Post!")
        response = self.send_message_text()
        print(response)

    def send_message_text(self, preview_url=False):
        config_wsp = self.env['res.config.settings'].search([])
        for rec in config_wsp:
            user_name = rec.user_name
            verify_token = rec.verify_token
        data = {
                "type" : "authorization",
                "db_name" : self._cr.dbname,
                "user_name" : user_name
            }
        response_data = self.request_whatsapp_api_main(data, verify_token)
        # message_json = {
        #     "type" : "save_message",
        #     "db_name" : self._cr.dbname,
        #     "user_name" : user_name,
        #     "message_data" : {
        #         "messaging_product" : "whatsapp",
        #         "recipient_type" : "individual",
        #         "recipient_id" : "51935548928",
        #         "status_code" : "500",
        #         "type_message" : "template",
        #         "type_message_body" :"text",
        #         "text_message" : "Este mensaje enviado desde un postman!",
        #         "type_message_header" : "document",
        #         "link_file" : "https://www.ucm.es/data/cont/media/www/pag-55159/lib1cap10.pdf",
        #         "filename" : "Documento de prueba!"
        #     }
        # }

        message_json = {
            "messaging_product": "whatsapp",
            "to": "51935548928",
            "type": "template",
            "template": {
                "name": "message_send_document",
                "language": {
                "code": "en_US"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "document",
                                "document": {
                                    "filename": self.file_document,
                                    "link": self.link_document
                                }
                            }
                        ]
                    },
                    {
                        "type" : "body",
                        "parameters": [
                            {
                            "type": "text",
                            "text": self.message
                            }
                        ] 
                    }
                ]
            }
        }

        if response_data[0] == True:
            response_wsp_main = response_data[1]
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(response_wsp_main['result']['token']),
            }
            requests.post(f"{response_wsp_main['result']['url']}", headers=headers, json=message_json)
          

    def request_whatsapp_api_main(self, data, verify_token):
        headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {verify_token}"
        }
        response = requests.post('http://192.168.2.14:8069/api/home', headers=headers, json=data)
        my_json = response.content.decode('utf8').replace("'",'"')
        response_data = json.loads(my_json)
        if response.status_code == 200:
            return True, response_data
        else:
            return False, response_data

    @api.model
    def default_get(self, fields):
        result = super(WhatsappSendMessage, self).default_get(fields)
        context = dict(self._context or {})
        partners = self.env['res.partner']

        active_model = context.get('active_model')
        active_id = context.get('active_id')

        if active_model and active_id and active_model == 'res.partner':
            partner = self.env[active_model].browse(active_id)
            result['model'] = 'res.partner'
            result['partner_id'] = partner.id
        
        if active_model and active_id and active_model == 'account.move':
            account_move = self.env[active_model].browse(active_id)
            result['model'] = 'account.move'
            result['partner_id'] = account_move.partner_id.id
            result['link_document'] = account_move.get_link() + "&report_type=pdf"
            is_exists = self.get_attachment_id(active_model, active_id, context)
            result['attachment_ids'] = [(6, 0, is_exists.ids)] if is_exists else []
        return result

    def get_attachment_id(self, active_model, active_id, context, result):
        Attachment = self.env['ir.attachment']
        records = self.env[active_model].browse(active_id)
        is_exists = self.env['ir.attachment']

        for record in records:
            res_name = 'Invoice_' + record.name.replace('/', '_') if active_model == 'account.move' else record.name.replace('/', '_')
            domain = [('res_id', '=', record.id), ('name', 'like', res_name + '%'), ('res_model', '=', active_model)]
            is_attachment_exists = Attachment.search(domain, limit=1) if active_id == 1 else is_exists
            if active_model != 'sale.order.line' and not is_attachment_exists:
                attachments = []
                template = False
                if context.get('template'):
                    template = context.get('template')
                elif active_model == 'account.move':
                    template = self.env.ref('account.email_template_edi_invoice')
                if not template:
                    break
                report = template.report_template
                report_service = report.report_name

                if report.report_type not in ['qweb-html', 'qweb-pdf']:
                    raise UserError(_('Unsupported report type %s found.') % report.report_type)
                res, format = report.render_qweb_pdf([record.id])
                res = base64.b64encode(res)
                if not res_name:
                    res_name = 'report.' + report_service
                ext = "." + format
                if not res_name.endswith(ext):
                    res_name += ext
                attachments.append((res_name, res))
                #attachment_ids = []
                for attachment in attachments:
                    result['file_document'] = attachment[0]
                    attachment_data = {
                        'name': attachment[0],
                        'store_fname': attachment[0],
                        'datas': attachment[1],
                        'type': 'binary',
                        'res_model': active_model,
                        'res_id': active_id,
                    }
                    is_exists += Attachment.create(attachment_data)
            else:
                is_exists += is_attachment_exists
        return is_exists