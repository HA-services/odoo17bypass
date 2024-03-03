# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CodaBox Bridge Wizard',
    'version': '1.0',
    'author': 'Odoo',
    'website': 'https://www.odoo.com/documentation/17.0/applications/finance/fiscal_localizations/belgium.html#codabox',
    'category': 'Accounting/Localizations',
    'description': 'CodaBox integration to retrieve your CODA and SODA files.',
    'depends': [
        'account_reports',
        'l10n_be_codabox_bridge',
    ],
    'auto_install': True,
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'wizard/connection_wizard.xml',
        'wizard/validation_wizard.xml',
    ],
    'license': 'OEEL-1',
}
