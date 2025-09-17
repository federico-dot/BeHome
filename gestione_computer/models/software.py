from odoo import models, fields

class Software(models.Model):
    _name = 'software'
    _description = 'modello del computer'

    name=fields.Char(string='name', required=True)
    descrizione=fields.Text(string='Descrizione')
    