from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from zope.interface import implements
from zope.component import queryUtility

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin

from plone.registry.interfaces import IRegistry

from pas.plugins.osiris5.interface import IOsirisHelper
from mrs5.max.browser.controlpanel import IMAXUISettings
import requests


class OsirisHelper(BasePlugin, Cacheable):
    """ Osiris PAS Plugin """

    meta_type = 'Osiris Helper'
    security = ClassSecurityInfo()

    implements(IOsirisHelper, IExtractionPlugin, IAuthenticationPlugin, IRolesPlugin)

    oauth_server = 'https://oauth.upcnet.es'

    _properties = (
        {
            'id': 'oauth_server',
            'label': 'Oauth Server URL',
            'type': 'string',
            'mode': 'w'
        },
    )

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    def extractCredentials(self, request):
        ''' Extract credentials from request '''
        creds = {}
        if request.get_header('X-Oauth-Username') and \
           request.get_header('X-Oauth-Token') and \
           request.get_header('X-Oauth-Scope'):
            username = request.get_header('X-Oauth-Username')
            token = request.get_header('X-Oauth-Token')
            scope = request.get_header('X-Oauth-Scope')

            data = dict(username=username, access_token=token, scope=scope)
            req = requests.post("{}/checktoken".format(self.oauth_server), data=data)
            if req.status_code == 200:
                creds['login'] = username

        # Login comunitats con username y oauth_token
        if request.form['__ac_name'] and request.form['__ac_password']:
            username = request.form['__ac_name']
            token = request.form['__ac_password']
            scope = 'widgetcli'

            data = dict(username=username, access_token=token, scope=scope)
            req = requests.post("{}/checktoken".format(self.oauth_server), data=data)
            if req.status_code == 200:
                creds['login'] = username

        return creds

    def authenticateCredentials(self, credentials):
        if credentials['extractor'] != self.getId():
            return None
        login = credentials['login']
        return (login, login)

    def getRolesForPrincipal(self, principal, request=None):
        """
            Grant api access if the current configured
            restricted user is the user currently logged in
        """
        registry = queryUtility(IRegistry)
        maxui_settings = registry.forInterface(IMAXUISettings)
        if maxui_settings.max_restricted_username == principal.getUserName():
            return ['Api']
        return []

InitializeClass(OsirisHelper)
