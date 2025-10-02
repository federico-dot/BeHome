from odoo import models,fields

class Modello(models.Model):
    _name="gestione_auto.modello"
    _description="Classe Modello"

    name=fields.Char(string="Nome Modello",required=True)
    descrizione=fields.Text(string="Descrizione Modello")
    active = fields.Boolean(string="Attivo", default=True)
    category = fields.Selection(
        [
            ('a', 'Categoria A'),
            ('b', 'Categoria B'),
            ('c', 'Categoria C'),
        ],
        string="Categoria",
        default='a'
    )
    price = fields.Float(string="Prezzo", digits=(6, 2))
    quantity = fields.Integer(string="Quantità", default=1)
