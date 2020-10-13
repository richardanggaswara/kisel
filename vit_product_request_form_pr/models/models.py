
from odoo import tools
from odoo import models, fields, api, _
import time
import logging
from odoo.tools.translate import _
from collections import defaultdict

_logger = logging.getLogger(__name__)

class ProductRequestFormPr(models.Model):
    _name = "vit.product.request"
    _inherit = ['vit.product.request','mail.thread']

    description = fields.Text(string="Description")
    requesto_id = fields.Many2one(comodel_name='res.users', string='Requester',required=True,default=lambda self: self.env.uid)