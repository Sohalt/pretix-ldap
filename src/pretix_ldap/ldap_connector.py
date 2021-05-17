from ldap3 import Server, Connection
from ldap3.utils.conv import escape_filter_chars
import re
import logging
from django import forms
from django.utils.translation import ugettext_lazy as _
from pretix.settings import config
from pretix.base.auth import BaseAuthBackend


logger = logging.getLogger(__name__)


class LDAPAuthBackend(BaseAuthBackend):
    def __init__(self):
        try:
            self.config = config
            self.server = Server(self.config.get('ldap', 'bind_url'))
            self.connection = Connection(self.server, self.config.get('ldap', 'bind_dn'), self.config.get('ldap', 'bind_password'), auto_bind=True)
            self.search_base = self.config.get('ldap', 'search_base')
        except KeyError:
            logger.error("Please specify bind_url, bind_dn, bind_password, and search_base in [ldap] section in pretix.cfg")
        self.search_filter_template = self.config.get('ldap', 'search_filter', fallback='(&(objectClass=inetOrgPerson)(mail={email}))')
        self.placeholders = re.findall('{([^{}]+)}', self.search_filter_template)
        if self.placeholders == {}:
            logger.error("Please specify at least one placeholder in your search_filter")
        self.email_attr = self.config.get('ldap', 'email_attr', fallback='mail')

    @property
    def identifier(self):
        return 'pretix_ldap'

    @property
    def verbose_name(self):
        return 'LDAP Authentication'

    @property
    def login_form_fields(self):
        # create text fields for all placeholders in the search string
        fields = {p: forms.CharField(label=p) for p in self.placeholders}
        fields['password'] = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
        # automatically focus the first field
        list(fields.values())[0].widget.attrs['autofocus'] = 'autofocus'
        return fields

    def form_authenticate(self, request, form_data):
        from pretix.base.models import User
        password = form_data['password']
        template_data = {p: escape_filter_chars(form_data[p]) for p in self.placeholders}
        filter = self.search_filter_template.format_map(template_data)
        if not self.connection.search(self.search_base, filter, attributes=[self.email_attr]):
            # user not found
            return None
        res = self.connection.response
        if len(res) != 1:
            # could not uniquely identify user
            logger.warn("Could not uniquely identify user. Check your search_filter")
            return None
        dn = res[0]['dn']
        emails = res[0]['attributes'][self.email_attr]
        # handle email being a single-valued attribute
        if isinstance(emails, str):
            emails = [emails]
        if len(emails) != 1:
            # could not uniquely identify user email
            logger.warn("Could not uniquely identify user email")
            return None
        email = emails[0]
        try:
            success = self.connection.rebind(user=dn, password=password)
        except: # noqa
            success = False
        bind_dn = self.config.get('ldap', 'bind_dn')
        bind_password = self.config.get('ldap', 'bind_password')
        if bind_dn and bind_password:
            self.connection.rebind(bind_dn, bind_password)
        if not success:
            # wrong password
            return None
        try:
            user = User.objects.get(email=email)
            if user.auth_backend == self.identifier:
                return user
            else:
                # user already registered with different backend
                return None
        except User.DoesNotExist:
            # user does not exist yet -> create new
            user = User(email=email)
            user.auth_backend = self.identifier
            user.save()
            return user
