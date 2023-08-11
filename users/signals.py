import jwt
import django
import allauth
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import (
    social_account_updated,
    social_account_added,
    social_account_removed,
    pre_social_login,
)
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from users.utilities.logger import get_configured_logger
from users.utilities.utilities import update_user_extradata
from decouple import config
from django.conf import settings

logger = get_configured_logger(loggername=__name__, filename="signals.log")


@receiver(django.contrib.auth.signals.user_logged_in)
def update_users_on_login(sender, user, request, **kwargs):
    update_user_extradata(user)


@receiver(pre_save, sender=get_user_model())
def update_users_on_save(sender, instance, **kwargs):
    if instance.pk:
        update_user_extradata(instance)


@receiver(django.contrib.auth.signals.user_logged_in)
def log_user_logged_in(sender, user, request, **kwargs):
    logger.info("User {} has logged in".format(user))


@receiver(allauth.account.signals.user_logged_in)
def log_allauth_user_logged_in(request, user, **kwargs):
    logger.debug("User {} has logged in via allauth".format(user))


@receiver(django.contrib.auth.signals.user_logged_out)
def log_user_logged_out(sender, user, request, **kwargs):
    logger.info("User {} has logged out".format(user))


def log_pre_social_login(request, sociallogin):
    try:
        logger.debug("Pre social login for User {}".format(sociallogin.user))
    except (get_user_model().DoesNotExist, AttributeError):
        logger.debug("Pre social login for non-existing User")


@receiver(pre_social_login)
def pre_social_login(request, sociallogin, **kwargs):
    log_pre_social_login(request, sociallogin=sociallogin)
    # The default OIDC provider does not provide the extra
    # data that CERN SSO returns (i.e. cern_roles).
    # For that reason we use the token from the login and decode it,
    # so that we can get all the extra info from it.
    key = jwt.PyJWKClient(settings.CERN_SSO_JWKS_URI).get_signing_keys()[0]
    sociallogin.account.extra_data = jwt.decode(
        jwt=sociallogin.token.token.encode("utf-8"),
        key=key.key,
        algorithms=["RS256"],
        audience=config("CERN_SSO_REGISTRATION_CLIENT_ID"),
    )
    # We now have to make sure that this data is saved in the
    # SocialAccount entry in the Database; there are two distinct
    # cases here:
    # 1. This is the first login of this specific user, and
    # there's no SocialAccount entry for them yet. In this case
    # (i.e. sociallogin.account.pk = None), at this point of the
    # login flow, this SocialAccount is NOT yet ready for saving,
    # as django-allauth is going to add some missing information
    # at a later step (during django-allauth's _add_social_account),
    # so let django-allauth save the account, later.
    #
    # 2. This is a login of a returning user we've already registered.
    # django-allauth has already updated and saved the account with the
    # stripped down information that the SSO returns (i.e. without
    # cern_roles) during account lookup, which happens *before* pre_social_login.
    # In this case, we have to update the extra info ourselves.
    if sociallogin.account.pk:
        sociallogin.account.save()


@receiver(social_account_added)
def log_social_account_added(request, sociallogin, **kwargs):
    try:
        logger.info(
            "Social Account {} has been added for User {}".format(
                sociallogin.account, sociallogin.user
            )
        )
    except (SocialAccount.DoesNotExist, get_user_model().DoesNotExist, AttributeError):
        logger.debug("Pre social login for non-existing User")


@receiver(social_account_updated)
def log_social_account_updated(request, sociallogin, **kwargs):
    try:
        logger.debug(
            "Social Account {} has been updated for User {}".format(
                sociallogin.account, sociallogin.user
            )
        )
    except (SocialAccount.DoesNotExist, get_user_model().DoesNotExist, AttributeError):
        logger.error("Something unexpected happened")


@receiver(social_account_removed)
def log_social_account_removed(request, socialaccount, **kwargs):
    try:
        logger.info(
            "Social Account {} has been removed from User {}".format(
                socialaccount, socialaccount.user
            )
        )
    except (get_user_model().DoesNotExist, AttributeError):
        logger.error("Something unexpected happened")


@receiver(django.contrib.auth.signals.user_login_failed)
def log_user_has_login_failed(sender, credentials, request, **kwargs):
    try:
        logger.warning(
            "User {} has failed to logged in".format(credentials.get("username"))
        )
    except AttributeError:
        logger.error("Username attribute does not exist!")
