{
    'name': 'Transformer Production Management',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Modul manajemen produksi transformator distribusi dan aksesori jaringan transmisi',
    'author': 'Odoo Developer',
    'depends': ['base', 'stock', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/sequence.xml',
        'views/production_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}