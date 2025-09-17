from odoo import models, fields, api

class ResPartners(models.Model):
    _inherit = 'res.partner'

    computer_ids=fields.One2many(comodel_name="prova_computer", inverse_name="utente_id", string="pc")
    
    numero_dispositivi=fields.Integer(string="numero dispositivi", compute="compute_numero_dispositivi")

    def action_view_computer(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'dispositivi di ' + self.complete_name,
            'res_model': "prova_computer",
            'view_mode': "list,form",
            'domain' : [('utente_id', '=', self.id)]
        }

    @api.depends("computer_ids")
    def compute_numero_dispositivi(self):
        for rec in self:
            if rec.computer_ids:
                rec.numero_dispositivi=len(rec.computer_ids)
            else:
                rec.numero_dispositivi=0
    
    