from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.fields import JSONField
from django.db import models
from django.contrib.auth.models import UserManager
from users.utilities.logger import get_configured_logger
from users.utilities.utilities import (
    get_highest_privilege_from_egroup_list,
    extract_egroups,
    get_or_create_group,
)

logger = get_configured_logger(loggername=__name__, filename="models.log")

class User(AbstractUser):
    """
    - adds extra information to the django User model
    - extends the default django User model using signals
    - grants user more access rights based on CERN e-groups the user is member of
    """

    GUEST = 0
    SHIFTER = 10
    SHIFTLEADER = 20
    EXPERT = 30
    ADMIN = 50

    USER_PRIVILEGE_GROUPS = (
        (GUEST, "Guests"),
        (SHIFTER, "Shifters"),
        (SHIFTLEADER, "Shift Leaders"),
        (EXPERT, "Experts"),
        (ADMIN, "Administrators"),
    )

    """
    Dictionary containing which e-group a user has to be member of, in order to 
    to gain a specific user privilege (e.g. Shift Leader or Admin)
    """
    criteria_groups_dict = {
        SHIFTER: [
            "cms-dqm-runregistry-offline-tracker-certifiers",
            "CMS-Shiftlist_shifters_DQM_Offline",
            "tkdqmdoctor-shifters",
            "CMS-Shiftlist_shifters_DQM_P5"],
        SHIFTLEADER: [
            "cms-tracker-offline-shiftleader",
            "cms-tracker-offline-shiftleaders",
            "tkdqmdoctor-shiftleaders",
            "cms-dqm-runregistry-admin-tracker",
        ],
        EXPERT: ["cms-dqm-certification-experts", "tkdqmdoctor-experts"],
        ADMIN: ["tkdqmdoctor-admins"],
    }

    objects = UserManager()

    extra_data = JSONField(verbose_name="extra data", default=dict)

    user_privilege = models.IntegerField(choices=USER_PRIVILEGE_GROUPS, default=GUEST)

    user_groups = dict((privilege, group) for privilege, group in USER_PRIVILEGE_GROUPS)

    def update_privilege(self):
        egroups = extract_egroups(self.extra_data)

        privilege = get_highest_privilege_from_egroup_list(
            egroups, self.criteria_groups_dict
        )

        if self.user_privilege < privilege:
            self.user_privilege = privilege
            logger.info(
                "User {} has been granted {} status".format(
                    self, self.get_user_privilege_display()
                )
            )

            if self.user_privilege >= self.SHIFTLEADER:
                self.is_staff = True
                logger.info("User {} is now staff".format(self))
                shift_leader_group = get_or_create_group(
                    self.user_groups[self.user_privilege]
                )
                self.groups.add(shift_leader_group)
                logger.info(
                    "User {} has been added "
                    "to the shift leader group".format(self)
                )

            if self.user_privilege >= self.ADMIN:
                self.is_superuser = True
                logger.info("User {} is now superuser".format(self))
        return self

    @property
    def is_guest(self):
        return self.user_privilege == self.GUEST

    @property
    def is_shifter(self):
        return self.user_privilege == self.SHIFTER

    @property
    def is_shiftleader(self):
        return self.user_privilege == self.SHIFTLEADER

    @property
    def is_expert(self):
        return self.user_privilege == self.EXPERT

    @property
    def is_admin(self):
        return self.user_privilege == self.ADMIN

    @property
    def has_shifter_rights(self):
        return (
            self.user_privilege
            in (self.SHIFTER, self.SHIFTLEADER, self.EXPERT, self.ADMIN)
            or self.is_staff
            or self.is_superuser
        )

    @property
    def has_shift_leader_rights(self):
        return (
            self.user_privilege in (self.SHIFTLEADER, self.EXPERT, self.ADMIN)
            or self.is_staff
            or self.is_superuser
        )

    def __str__(self):
        return self.get_full_name() + " (" + self.username + ")"
