from .ldap_connector import LDAPAuthBackend  # noqa
from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    name = "pretix_ldap"
    verbose_name = "pretix LDAP"

    class PretixPluginMeta:
        name = gettext_lazy("pretix LDAP")
        author = "sohalt"
        description = gettext_lazy("LDAP authentication backend for pretix")
        visible = True
        version = "0.2.5"
        compatibility = "pretix>=2023.06.0"


default_app_config = "pretix_ldap.PluginApp"
