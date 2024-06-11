###################################---django_auth_ldap---######################################
import ldap
import os
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

if int(os.environ.get('USE_LDAP', '0')) == 1:

    # Basic configuration.
    AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI', '')
    AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN', '')
    AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD','')
    AUTH_LDAP_ROOT_DN = os.environ.get('AUTH_LDAP_ROOT_DN','')
    AUTH_LDAP_USERS_OU = os.environ.get('AUTH_LDAP_USERS_OU','')
    AUTH_LDAP_SU_CN = os.environ.get('AUTH_LDAP_SU_CN','')


    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    # Either AUTH_LDAP_USER_DN_TEMPLATE or AUTH_LDAP_USER_SEARCH need to be set
    # AUTH_LDAP_USER_DN_TEMPLATE = "(sAMAccountName=%(user)s),dc=int,dc=bgkb,dc=ru"
    AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_USERS_OU + ',' + AUTH_LDAP_ROOT_DN,
        ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"
        )

    AUTH_LDAP_USER_ATTR_MAP = {
        "username": "sAMAccountName",
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail"
    }

    AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
    AUTH_LDAP_CONNECTION_OPTIONS = {ldap.OPT_REFERRALS: 0}


    #Set up the basic group parameters.
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(AUTH_LDAP_ROOT_DN,
        ldap.SCOPE_SUBTREE, "(objectClass=Group)"
    )

    # AUTH_LDAP_MIRROR_GROUPS = True

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        # "is_active": ("OU=ГБУЗ АО БГКБ,DC=int,DC=bgkb,DC=ru",
        #               ),
        # # "is_staff": ("ou=mathematicians,dc=example,dc=com",
        # #              "ou=scientists,dc=example,dc=com",
        # #              ),
        "is_superuser": AUTH_LDAP_SU_CN + ',' + AUTH_LDAP_ROOT_DN
    }

    AUTH_LDAP_FIND_GROUP_PERMS = True
    AUTH_LDAP_CACHE_GROUPS = True
    # AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = 1 # 1 hour

    # Keep ModelBackend around for per-user permissions and maybe a local
    # superuser.

    import logging
    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.ERROR)

    AUTHENTICATION_BACKENDS = (
        'django_auth_ldap.backend.LDAPBackend',
        'rules.permissions.ObjectPermissionBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

###############################################################################################
