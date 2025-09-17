from odoo import models, fields

class Prova_computer(models.Model):
    _name = 'prova_computer'
    _description = 'gestione computer dipendenti'

    name = fields.Char(string='name', required=True)
    marca_id = fields.Many2one(string='Marca', comodel_name='marca') 
    modello_id = fields.Many2one(string='Modello', comodel_name='modello', domain="[('marca', '=' , marca_id)]")
    capacita1 = fields.Integer(string='Capacità HDR o SSD', required=False)
    capacita2 = fields.Selection([("4GB", "4GB"),("8GB", "8GB"),("16GB", "16GB"),("24GB", "24GB"),("32GB", "32GB")], string="RAM")             
    processore = fields.Char(string='Processore', required=True)
    data_acquisto = fields.Date(string='Data acquisto', required=False)
    garanzia = fields.Date(string='Garanzia', required=False)
    utente_id = fields.Many2one(string='Utente collegato', comodel_name='res.partner', domain="[('user_ids', '!=', False)]")
    sistema_operativo = fields.Selection([("Win10", "Win10"),("Win11", "Win11")])
    software_ids = fields.Many2many('software', string='software')
    responsabile = fields.Many2one(string='Responsabile', comodel_name='res.users')