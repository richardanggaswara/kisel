from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class sale(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'


    billplan_id = fields.Many2one(comodel_name="vit_project_billplan.bill_plan", string="Billplan", required=False, )