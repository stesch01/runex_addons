# -*- coding: utf-8 -*-

import logging
import werkzeug

import openerp
from openerp.addons.auth_signup.res_users import SignupError
from openerp import http
from openerp.http import request
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

import openerp.addons.web.controllers.main as main

import sys
reload(sys)
sys.setdefaultencoding("utf8")

class AuthSignupHomeSplitName(main.Home):

    @http.route('/web/signup', type='http', auth='public', website=True)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        name = qcontext.get('name')
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                #joining fields for a final username - name + surname
                surname = qcontext.get('surname')
                if name and surname:
                    name = str(name).rstrip()
                    surname = str(surname).lstrip()
                    legal_name = name + ' ' + surname
                    qcontext.update({'name': legal_name})
                self.do_signup(qcontext)
                return super(AuthSignupHomeSplitName, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error(e.message)
                    qcontext['error'] = _("Could not create a new account.")
        #if there was any errors we ovewriting name with originaly entered in form
        qcontext.update({'name': name})
        return request.render('auth_signup.signup', qcontext)
