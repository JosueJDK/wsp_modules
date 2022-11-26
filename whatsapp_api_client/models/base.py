from odoo import api, fields, models, _
from passlib.context import CryptContext
import logging
_logger = logging.getLogger(__name__)

class base(models.TransientModel):
    _inherit = "res.config.settings"

    user_name = fields.Char(string="User name", required=True)
    verify_token = fields.Char(string="Token", required=True)

    @api.model
    def get_values(self):
        res = super(base, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        res['user_name'] = param.sudo().get_param('whatsapp_api_client.user_name')
        res['verify_token'] = param.sudo().get_param('whatsapp_api_client.verify_token')
        return res

    def set_values(self):
        super(base, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('whatsapp_api_client.user_name', self.user_name)
        self.env['ir.config_parameter'].sudo().set_param('whatsapp_api_client.verify_token', self.verify_token)


    def _encrypted_password(self, password):
        pwd_context = CryptContext(schemes=['pbkdf2_sha512'], deprecated="auto")
        return pwd_context.hash(password)

    @api.model
    def create(self, vals):
        vals['verify_token'] = self._encrypted_password(vals['verify_token'])
        return super(base, self).create(vals)