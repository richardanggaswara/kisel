# 
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
import time
import logging


_logger = logging.getLogger(__name__)
DOC_STATES =[('draft','Draft'),
		('open','Need Approval'), 
		# ('confirmed','Approved'),
		('unread','Unread'),
        ('read','Read')]
class doc(models.Model):
	_name 		= "eo.doc"
	_inherit 	= ['mail.thread']
	_description = "Surat"

	name = fields.Char(string="Nomor", readonly=True)
	subject	= fields.Char(string="Perihal", required=True, readonly=True, states={'draft': [('readonly', False)]})
	body = fields.Text(string="Isi Surat", required=True , readonly=True, states={'draft': [('readonly', False)]})
	user_id = fields.Many2one(comodel_name='res.users', string="Dari", required=True, readonly=True, states={'draft': [('readonly', False)]})
	to_user_ids = fields.One2many(comodel_name='eo.to_user',inverse_name='doc_id',string="Kepada", ondelete="cascade", required=True, readonly=True, states={'draft': [('readonly', False)]})
	cc_user_ids	= fields.One2many(comodel_name='eo.cc_user',inverse_name='doc_id',string="Tembusan", ondelete="cascade", readonly=True, states={'draft': [('readonly', False)]})
	date = fields.Date(default=lambda self: time.strftime("%Y-%m-%d"),string="Tanggal", required=True, readonly=True, states={'draft': [('readonly', False)]})
	doc_type_id	= fields.Many2one(comodel_name='eo.doc_type', string="Klasifikasi", required=True, readonly=True, states={'draft': [('readonly', False)]})
	doc_template_id = fields.Many2one(comodel_name='eo.doc_template', string="Template Surat", required=True, readonly=True, states={'draft': [('readonly', False)]})
	read_status = fields.Boolean(string="Read", readonly=True)
	state = fields.Selection(default=DOC_STATES[0][0],selection=DOC_STATES,string="Status",readonly=True, required=True)
	doc_history = fields.One2many(comodel_name='eo.doc_history',inverse_name='doc_id',string="History", ondelete="cascade", readonly=True)
	parent_id = fields.Many2one(comodel_name='eo.doc', string="Sumber Surat")
	

	#########################################################################
	#########################################################################
	def create(self, cr, uid, vals, context=None):
		name = self.pool.get('ir.sequence').get(cr, uid, 'eo.doc') or '/'
		vals.update({
			'name':name,
		})
		new_id = super(doc, self).create(cr, uid, vals, context=context)
		self.insert_history(cr, uid, new_id, 'Created')

		return new_id
	

	#########################################################################
	# read doc dan update status read di to_user_id dan cc_user_id
	# jika semua to_user_id sudah read maka update doc state = read 
	#########################################################################
	def read(self, cr, uid, ids, fields=None, context=None, load='_classic_read'):
		if len(ids) == 1:
			# import pdb; pdb.set_trace()
			# update status read utk to_user yang matching doc_id dan uid nya
			to_user_obj = self.pool.get('eo.to_user')
			to_user_id  = to_user_obj.search(cr, uid, [('doc_id','=',ids[0]), ('user_id','=',uid)], context=context)
			if to_user_id:
				to_user_obj.write(cr, uid, to_user_id , {'read_status': True}, context=context)
				self.insert_history(cr, uid, ids[0], 'Read (to)')

			# update status read utk cc_user yang matching doc_id dan uid nya
			cc_user_obj = self.pool.get('eo.cc_user')
			cc_user_id  = cc_user_obj.search(cr, uid, [('doc_id','=',ids[0]), ('user_id','=',uid)], context=context)
			if cc_user_id:
				cc_user_obj.write(cr, uid, cc_user_id , {'read_status': True}, context=context)
				self.insert_history(cr, uid, ids[0], 'Read (cc)')

			#update status doc = read jika semua to_user_ids sudah read_status=True
			st=''
			to_user_ids = to_user_obj.search(cr, uid, [('doc_id','=',ids[0])], context=context)
			# import pdb; pdb.set_trace()
			for to_user_id in to_user_obj.browse(cr, uid, to_user_ids, context=context):
				if to_user_id.read_status == True:
					st ='read'
				else:
					st = ''
					break;
			
			if st=='read':
				self.write(cr, uid, ids, {'state':st}, context=context)
				self.insert_history(cr, uid, ids[0], 'State updated to Read')

		#parent read
		res = super(doc, self).read(cr, uid, ids, fields=fields, context=context, load=load)
		return res


	#########################################################################
	# replace tokens in body
	#########################################################################
	def replace_tokens(self, cr, uid, id, context=None):
		return 

	#########################################################################
	# insert history
	#########################################################################
	def insert_history(self, cr, uid, doc_id, name, context=None):
		doc_history_obj = self.pool.get('eo.doc_history')

		data = {
			'name'		: name ,
			'user_id'	: uid,
			'doc_id'	: doc_id,
		}

		res = doc_history_obj.create(cr, uid, data, context=context)
		return res 

	#########################################################################
	# actions
	#########################################################################

	def action_draft(self,cr,uid,ids,context=None):
		self.insert_history(cr, uid, ids[0], 'Set to Draft')
		return self.write(cr,uid,ids,{'state':DOC_STATES[0][0]},context=context)
	
	def action_open(self,cr,uid,ids,context=None):
		for doc in self.browse(cr, uid, ids, context=context):
			if not doc.to_user_ids:
				raise osv.except_osv(_('Error'),_("Pilih minimal satu tujuan surat") ) 

		self.insert_history(cr, uid, ids[0], 'Set to Need Approval')
		return self.write(cr,uid,ids,{'state':DOC_STATES[1][0]},context=context)
		
	# def action_approve(self,cr,uid,ids,context=None):
	# 	self.insert_history(cr, uid, ids[0], 'Set to Approved')
	# 	return self.write(cr,uid,ids,{'state':DOC_STATES[2][0]},context=context)
		
	def action_send(self,cr,uid,ids,context=None):

		doc = self.browse(cr, uid, ids, context=context)[0]

		partner_ids = [ to_user.user_id.partner_id.id for to_user in doc.to_user_ids ]
		partner_ids += [ cc_user.user_id.partner_id.id for cc_user in doc.cc_user_ids ]

		body = _("Anda mendapat Surat No:%s dari %s, silahkan dibuka") % (doc.name, doc.user_id.name)
		self.message_post(cr, uid, ids , body=body, partner_ids=partner_ids, context=context)

		self.insert_history(cr, uid, ids[0], 'Set to Unread')
		return self.write(cr,uid,ids,{'state':DOC_STATES[2][0]},context=context)
	
	def action_read(self,cr,uid,ids,context=None):
		self.insert_history(cr, uid, ids[0], 'Set to Read')
		return self.write(cr,uid,ids,{'state':DOC_STATES[3][0]},context=context)
			
	def action_reply(self,cr,uid,ids,context=None):
		'''
		redirect to eo.doc form view with prefilled values 
		from the old doc
		'''

		######################################################################
		# get the old doc
		######################################################################
		data = self.browse(cr, uid, ids, [])[0]

		######################################################################
		# set defautl values for the redirect 
		######################################################################
		context.update({
			'default_parent_id' : data.id,
			'default_user_id'   : uid,
			'default_to_user_ids' : [(0, 0, {'user_id': data.user_id.id })]
		})

		######################################################################
		# history 
		######################################################################
		self.insert_history(cr, uid, ids[0], 'Replied')

		######################################################################
		# return and show the view  
		######################################################################
		return {
			'name': _('Reply Surat'),
			'view_type': 'form',
			"view_mode": 'form',
			'res_model': 'eo.doc',
			'type': 'ir.actions.act_window',
			'context': context,
		}

	def action_forward(self,cr,uid,ids,context=None):
		'''
		redirect to eo.doc form view with prefilled values 
		from the old doc
		'''

		######################################################################
		# get the old doc
		######################################################################
		data = self.browse(cr, uid, ids, [])[0]

		######################################################################
		# set defautl values for the redirect 
		######################################################################
		context.update({
			'default_parent_id' : data.id,
			'default_user_id'   : uid,
		})

		######################################################################
		# history 
		######################################################################
		self.insert_history(cr, uid, ids[0], 'Forwarded')

		######################################################################
		# return and show the view  
		######################################################################
		return {
			'name': _('Reply Surat'),
			'view_type': 'form',
			"view_mode": 'form',
			'res_model': 'eo.doc',
			'type': 'ir.actions.act_window',
			'context': context,
		}		
		return 

	#########################################################################
	# doc template changes
	#########################################################################
	def onchange_doc_template(self, cr, uid, ids, doc_template_id ):
		# return harus berupa dict yang berisi key = 'value'
		# setiap value berupa dict yang berisi nilai dari field lain
		#   yang mau diupdate 
		doc_template = self.pool.get('eo.doc_template').browse(cr, uid, doc_template_id, context=None)

		results = {
			'value' : {
				'body' : doc_template.body
			}
		}
		return results

class to_user(models.Model):
	_name 		= "eo.to_user"
	_rec_name   = 'user_id'
	
	user_id = fields.Many2one(comodel_name='res.users', string="User")
	doc_id = fields.Many2one(comodel_name='eo.doc', string="Surat")
	read_status = fields.Boolean(string="Read")


class cc_user(models.Model):
	_name 		= "eo.cc_user"
	_rec_name   = 'user_id'
	
	user_id = fields.Many2one(comodel_name='res.users', string="User")
	doc_id = fields.Many2one(comodel_name='eo.doc', string="Surat")
	read_status = fields.Boolean(string="Read")
	

class doc_type(models.Model):
	_name 		= "eo.doc_type"

	code = fields.Char(string="Kode", required=True)	
	name = fields.Char(string="Nama", required=True)		
	

class doc_template(models.Model):
	_name 		= "eo.doc_template"
	
	code = fields.Char(string="Kode", required=True)		
	name = fields.Char(string="Nama", required=True)		
	body = fields.Text(string="Isi", required=True)		
	

class doc_history(models.Model):
	_name 		= "eo.doc_history"
	
	name = fields.Char(string="History")
	user_id = fields.Many2one(comodel_name='res.users', string="By")
	doc_id = fields.Many2one(comodel_name='eo.doc', string="Surat")
	

