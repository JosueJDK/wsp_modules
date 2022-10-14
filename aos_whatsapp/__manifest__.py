# See LICENSE file for full copyright and licensing details.

{
    'name': 'Whatsapp Client',
    'version': '13.0.0.1.0',
    'license': 'OPL-1',
    'author': "VMC SOLUTIONS",
    'sequence': 1,
    'website': 'https://www.alphasoft.co.id/',
    'summary': 'This module is used for Whatsapp Client Connection',
    'category': 'Extra Tools',
    'depends': ['mail','base_setup','contacts','account','base'],
    'data': [
        'views/res_partner_view.xml',
        'wizard/whatsapp_message_view.xml',
        'views/account_invoice.xml',
        'views/account_payment.xml',
        'views/res_config_settings_view.xml',
        'views/views.xml'
    ]
}
