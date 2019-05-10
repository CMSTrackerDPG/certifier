import allauth
import django
from allauth.account.signals import user_logged_in
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.signals import social_account_updated, \
    social_account_added, social_account_removed, pre_social_login
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from users.utilities.logger import get_configured_logger
from users.utilities.utilities import update_user_extradata

logger = get_configured_logger(loggername=__name__, filename="signals.log")

@receiver(django.contrib.auth.signals.user_logged_in)
def update_users_on_login(sender, user, request, **kwargs):
    update_user_extradata(user)
    user.save()


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


@receiver(pre_social_login)
def log_pre_social_login(request, sociallogin, **kwargs):
    try:
        logger.debug("Pre social login for User {}".format(sociallogin.user))
    except (get_user_model().DoesNotExist, AttributeError):
        logger.debug("Pre social login for non-existing User")


@receiver(social_account_added)
def log_social_account_added(request, sociallogin, **kwargs):
    try:
        logger.info("Social Account {} has been added for User {}"
                    .format(sociallogin.account, sociallogin.user))
    except (SocialAccount.DoesNotExist, get_user_model().DoesNotExist, AttributeError):
        logger.debug("Pre social login for non-existing User")


@receiver(social_account_updated)
def log_social_account_updated(request, sociallogin, **kwargs):
    try:
        logger.debug("Social Account {} has been updated for User {}"
                     .format(sociallogin.account, sociallogin.user))
    except (SocialAccount.DoesNotExist, get_user_model().DoesNotExist, AttributeError):
        logger.error("Something unexpected happened")


@receiver(social_account_removed)
def log_social_account_removed(request, socialaccount, **kwargs):
    try:
        logger.info("Social Account {} has been removed from User {}"
                    .format(socialaccount, socialaccount.user))
    except (get_user_model().DoesNotExist, AttributeError):
        logger.error("Something unexpected happened")


@receiver(django.contrib.auth.signals.user_login_failed)
def log_user_has_login_failed(sender, credentials, request, **kwargs):
    try:
        logger.warning(
            "User {} has failed to logged in".format(credentials.get("username")))
    except AttributeError:
        logger.error("Username attribute does not exist!")
