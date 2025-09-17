from odoo import models, fields

class ResMarca(models.Model):
    _name = 'marca'
    _description = 'marca del computer'

    name=fields.Char(string='name', required=True)
    descrizione=fields.Text(string='Descrizione')
    