from openerp.addons.web import http
from openerp.http import request
from openerp import _
#----------------------------------------------
import base64
import logging
import json

_logger = logging.getLogger(__name__)

class upload(http.Controller):

	@http.route('/upload/files', type='http', auth='user', csrf=False)
	def upload(self, id, model, files, csrf_token):
		_logger.info('... begin uploads .....')
		Model = request.session.model('ir.attachment')
		out = """<script language="javascript" type="text/javascript">
		var win = window.top.window;
		win.jQuery(win).trigger(%s, %s);
		</script>"""
		print '-' * 100
		if id and model:
			attachment_id = Model.create({
				'name': files.filename,
				'datas': base64.encodestring(files.read()),
				'datas_fname': files.filename,
				'res_model': model,
				'res_id': id,
			}, request.context)
			
			_logger.info('...attachment_id %s .....' % attachment_id)
			_logger.info('... end uploads .....')
			return json.dumps({
				'model': model,
				'id': int(id),
			})
		else:
			_logger.info('... null current_id and model .....')
			_logger.info('... end uploads .....')
			return 'False'