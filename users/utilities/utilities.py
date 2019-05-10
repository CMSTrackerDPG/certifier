import datetime
import decimal
import re

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from django.utils.safestring import mark_safe
from terminaltables import AsciiTable

from users.utilities.logger import get_configured_logger

logger = get_configured_logger(loggername=__name__, filename="utilities.log")

def extract_egroups(json_data):
    """
    Returns the E-Groups in a JSON Dictionary
    """
    return json_data.get("groups")


def get_highest_privilege_from_egroup_list(egroups, criteria_dict):
    """
    Compares every egroup in egroups with the criteria_dict
    and returns the highest criteria found
    """
    highest_privilege = 0
    for privilege, criteria_list in criteria_dict.items():
        if any(egroup in criteria_list for egroup in egroups):
            if privilege > highest_privilege:
                highest_privilege = privilege
    return highest_privilege


def get_or_create_group(group_name):
    try:
        g = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        user_permissions = Permission.objects.filter(
                content_type__model="user"
        )
        users_permissions = Permission.objects.filter(
            content_type__app_label="users"
        )
        oms_permissions = Permission.objects.filter(
            content_type__app_label="oms"
        )
        certifier_permissions = Permission.objects.filter(
            content_type__app_label="certifier"
        )
        all_permissions = Permission.objects.all()

        g = Group.objects.create(name=group_name)

        if group_name == "Shift Leaders" or group_name == "Experts":
            for permission in user_permissions:
                g.permissions.add(permission)
            for permission in users_permissions:
                g.permissions.add(permission)
            for permission in oms_permissions:
                g.permissions.add(permission)
            for permission in certifier_permissions:
                g.permissions.add(permission)
        elif group_name == "Administrators":
            for permission in all_permissions:
                g.permissions.add(permission)

        g.save()
    return g

def update_user_extradata(user):
    if user:  # Only already existing users
        try:
            socialaccount = SocialAccount.objects.get(user=user)
            if user.extra_data != socialaccount.extra_data:
                user.extra_data = socialaccount.extra_data
                user = user.update_privilege()
                logger.info("Extra data have been updated for {}".format(user))
        except SocialAccount.DoesNotExist:
            logger.warning("No SocialAccount exists for User {}".format(user))
    else:
        logger.info("Cannot update extradata for non existing User {}".format(user))
