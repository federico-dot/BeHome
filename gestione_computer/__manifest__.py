{
    'name': 'gestione computer',
    'version': '1.0',
    'author': 'Mario',
    'depends': ['base'],
    'installable': True,
    'application': False,
    'data':[
        'views/computer_view.xml',
        'views/marca_view.xml',
        'views/modello_view.xml',
        'views/software_view.xml',
        'views/res_partners_view.xml',
        'security/ir.model.access.csv'
     ]
}