{
    'name': 'Purchase Request Inherit',
    'version': '1.0',

    'website': 'https://www.centione.com',
    'depends': ['purchase', 'purchase_request', 'purchase_request_to_rfq', 'hr'],
    'data': [
        'security/purchase_request_inherit_security_view.xml',
        'security/ir.model.access.csv',
        'views/purchase_request_inherit_view.xml',

    ]
}