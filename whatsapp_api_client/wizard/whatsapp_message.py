# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import base64, logging
from odoo.exceptions import UserError
from .WhatsApp.WhatsApp import WhatsAppMain

logging.getLogger(__name__)

class WhatsappSendMessage(models.TransientModel):
    _name = 'whatsapp.send.message'
    _description = "Whatsapp Message"

    partner_id = fields.Many2one('res.partner', string='Contact', require=True)
    subject = fields.Char('Subject')
    message = fields.Text(require=True)
    model = fields.Char('Object')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'whatsapp_send_message_ir_attachments_rel',
        'wizard_id', 'attachment_id', 'Attachments')
    number_phone = fields.Char(string='Phone Address', require=True)
    link_document = fields.Char(string="Link PDF")
    file_document = fields.Char(string="PDF name")
    template_id = fields.Many2one('whatsapp.api.client.messages.templates', 'Use template', index=True)

    @api.onchange('partner_id')
    def get_phone_number(self):
        number_phone = self.partner_id.phone
        number_mobile = self.partner_id.mobile
        if number_phone:
            print(number_phone)
            self.number_phone = number_phone
        if number_mobile:
            print(number_mobile)
            self.number_phone = number_mobile
        else:
            self.number_phone = ""

    def whatsapp_message_post(self):
        if not self.number_phone or self.number_phone[0] != "9" or len(self.number_phone) != 9 or self.number_phone == "":
            raise UserError(_('El numero ingresado no es valido!'))
        if not self.message:
            raise UserError(_('El cuerpo del mensaje no puede estar vacio!'))
        if not self.template_id:
            raise UserError(_('Debe seleccionar una plantilla!'))
        else:
            logging.info("Mensaje enviado!")
            self._request_whatsapp_api_main()
    
    def create_message_whatsapp_client(self, data_save_message):
        model_message = self.env['whatsapp.api.client.messages'].sudo()
        new_message = {
            'name' : '',
            'partner_id' : self.partner_id.id,
            'messaging_product' : data_save_message['message_data']['messaging_product'],
            'recipient_type' : data_save_message['message_data']['recipient_type'],
            'recipient_id' : data_save_message['message_data']['recipient_id'],
            'status_code' : str(data_save_message['message_data']['status_code']),
            'type_message' : data_save_message['message_data']['type_message'],
            'text_message' : data_save_message['message_data']['text_message'],
            'link_file' : data_save_message['message_data']['link_file'],
            'filename' : data_save_message['message_data']['filename'],
        }
        model_message.create(new_message)

    def _request_whatsapp_api_main(self):
        config_wsp = self.env['res.config.settings'].search([])
        for rec in config_wsp:
            user_name = rec.user_name
            token_verify = rec.verify_token
        db_name = self._cr.dbname

        new_object = WhatsAppMain(user_name, token_verify, db_name)
        authorization_request = new_object.request_authorization_whatsapp()
        
        logging.info("Received webhook data: %s", authorization_request)
        if authorization_request[0] == True:
            component_header = False
            component_body = False
            if self.model == "res.partner":
                message_json = new_object._send_message_template(self.template_id.name, self.number_phone)

            elif self.model == "account.move":
                component_header = new_object.create_message_components_header(self.file_document, self.link_document)
                logging.info("Received webhook component_header: %s", component_header)
                component_body = new_object.create_message_components_body(self.message)
                logging.info("Received webhook component_body: %s", component_body)
                components = [component_header, component_body]
                logging.info("Received webhook components: %s", components)
                message_json = new_object._send_message_template(self.template_id.name, self.number_phone, components)
                logging.info("Received webhook message_json: %s", message_json)
            else:
                message_json = new_object._send_message_template('hello_world', self.number_phone)

            logging.info("Received webhook authorization_request: %s", authorization_request)
            response_wasapi = new_object.send_message_whatsapp(authorization_request, message_json)
            logging.info("Received webhook response_wasapi: %s", response_wasapi)
            data_save_message = new_object._generate_save_message_json(response_wasapi[1], self.number_phone, component_body, component_header)
            logging.info("Received webhook data_save_message: %s", data_save_message)
            logging.info("Received webhook request_save_message_whatsapp: %s", new_object.request_save_message_whatsapp(data_save_message))
            logging.info("Received webhook self.create_message_whatsapp_client: %s", self.create_message_whatsapp_client(data_save_message))
            if response_wasapi[1] != 200:
                raise UserError(_('El mensaje no fue enviado correctamente!!'))
        else:
            raise UserError(_('No tiene autorizacion para enviar mensajes contacte con la empresa proveedora para mas informacion!'))
            
    @api.model
    def default_get(self, fields):
        result = super(WhatsappSendMessage, self).default_get(fields)
        context = dict(self._context or {})

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
            is_exists = self.get_attachment_id(active_model, active_id, context, result)
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