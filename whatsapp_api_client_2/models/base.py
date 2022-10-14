from odoo import api, fields, models, _

class base(models.TransientModel):
    _inherit = "res.config.settings"

    user_name = fields.Char(string="User name registreted in whatsapp.api.main", required=True)
    verify_token = fields.Char(string="Token registreted in whatsapp.api.main", required=True)

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
