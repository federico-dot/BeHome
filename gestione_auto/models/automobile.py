from odoo import models,fields,api

class Automobile(models.Model):
    _name="gestione_auto.automobile"
    _description="Classe Automobile"

    marca=fields.Many2one(string="Marca",comodel_name="gestione_auto.marca",required=True) 
    modello=fields.Many2one(string="Modello",comodel_name="gestione_auto.modello", required=True) 
    descrizione=fields.Text(string="Descrizione")
    targa=fields.Char(string="Targa",required=True)
    data_immatricolazione=fields.Date(string="Data Immatricolazione")
    anno_immatricolazione=fields.Char(string="Anno Immatricolazione",compute="Get_anno",store=True)
    colore=fields.Char(string="Colore",required=True, default="#FFFFFF")
    prezzo=fields.Float(string="Prezzo",required=True)


    name = fields.Char(string="Nome Visualizzato", compute="Nome_visualizzato", default="Nome Veicolo")

    @api.depends("marca", "modello")
    def Nome_visualizzato(self):
        for record in self:
            record.name = f"{record.marca} {record.modello}"

    @api.depends("data_immatricolazione")
    def Get_anno(self):
        for record in self:
            if record.data_immatricolazione:
                record.anno_immatricolazione = record.data_immatricolazione.year
            else:
                record.anno_immatricolazione = False
                