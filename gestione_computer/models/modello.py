from odoo import models, fields

class Modello(models.Model):
    _name = 'modello'
    _description = 'modello del computer'

    name=fields.Char(string='name', required=True)
    descrizione=fields.Text(string='Descrizione')
    marca=fields.Many2one(string='Marca', comodel_name='marca')
