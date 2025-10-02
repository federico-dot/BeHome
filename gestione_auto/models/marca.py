from odoo import models, fields, api
from odoo.exceptions import ValidationError
import imghdr
import base64

class Marca(models.Model):
    _name = "gestione_auto.marca"
    _description = "Classe Marca"

    name = fields.Char(string="Nome Marca", required=True)
    descrizione = fields.Text(string="Descrizione Marca")
    paese_origine = fields.Char(string="Paese di Origine")
    anno_fondazione = fields.Integer(string="Anno di Fondazione")
    logo = fields.Binary(string="Logo Marca")

    @api.constrains('logo')
    def check_foto(self):
        MAX_SIZE_MB = 2
        for record in self:
            if record.logo:
                data = base64.b64decode(record.logo)
                tipo_file = imghdr.what(None, h=data)
                
                if tipo_file not in ["jpeg", "png"]:
                    raise ValidationError("Il logo deve essere un'immagine PNG o JPEG")
                
                size_mb = len(data) / (1024 * 1024)
                if size_mb > MAX_SIZE_MB:
                    raise ValidationError("Immagine troppo grande, non deve superare i 2 MB")
