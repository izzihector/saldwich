# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError


class ItemCardWizard(models.TransientModel):
    """Item Card"""

    _name = "item.card.wizard"
    _description = "Item Card Wizard"

    date_from = fields.Datetime(string='Date From', required=True)
    date_to = fields.Datetime(string='Date To', default=fields.Datetime.now(), required=True)
    product_id = fields.Many2one('product.product', string='Product')
    report_view = fields.Selection([('detailed', 'Detailed'), ('total', 'Total')],
                                   default='detailed', string='Report View', required=True,
                                   help='Choose how you want to view the report(detailed for viewing transactions - total for viewing without transactions)')
    show_cost = fields.Boolean(string='Show Cost', help='Show Cost Columns')

    @api.multi
    def view_report(self):
        self.ensure_one()
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('state', '=', 'done')]
        if self.product_id:
            domain += [('product_id', '=', self.product_id.id)]

        without_cost_tree_view_id = self.env.ref('bi_item_card_report.view_item_card_without_cost_tree').id
        cost_tree_view_id = self.env.ref('bi_item_card_report.view_item_card_with_cost_tree').id

        if self.show_cost:
            tree_view_id = cost_tree_view_id
        else:
            tree_view_id = without_cost_tree_view_id
        if self.report_view == 'detailed':
            default_product_group = False
        else:
            default_product_group = True
        # We pass `to_date` in the context so that `qty_available` will be computed across
        # moves until date.
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_mode': 'tree',
            'name': _('Item Card'),
            'res_model': 'stock.move.line',
            'domain': domain,
            'context': dict(self.env.context, date_from=self.date_from, date_to=self.date_to,
                            product_id=self.product_id.id or False, report_view=self.report_view,
                            show_cost=self.show_cost, search_default_groupby_product_id=default_product_group),
        }
        return action

    @api.onchange('report_view')
    def onchange_report_view(self):
        self.product_id = False
        self.show_cost = False
