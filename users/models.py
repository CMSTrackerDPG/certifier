from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.fields import JSONField
from django.db import models

class User(AbstractUser):
    """
    Do NOT instantiate this manually!
    It will be automatically created/updated when a User instance is created/updated
    - adds extra information to the django User model
    - extends the default django User model using signals
    - grants user more access rights based on CERN e-groups the user is member of
    """

    GUEST = 0
    SHIFTER = 10
    SHIFTLEADER = 20
    EXPERT = 30
    ADMIN = 50

    USER_PRIVILEGE_CHOICES = (
        (GUEST, "Guest"),
        (SHIFTER, "Shifter"),
        (SHIFTLEADER, "Shift Leader"),
        (EXPERT, "Expert"),
        (ADMIN, "Administrator"),
    )

    SHIFT_LEADER_GROUP_NAME = "Shift leaders"

    """
    Dictionary containing which e-group a user has to be member of, in order to 
    to gain a specific user privilege (e.g. Shift Leader or Admin)
    """
    criteria_groups_dict = {
        SHIFTER: ["CMS-Shiftlist_shifters_DQM_Offline", "tkdqmdoctor-shifters"],
        SHIFTLEADER: [
            "cms-tracker-offline-shiftleader",
            "cms-tracker-offline-shiftleaders",
            "tkdqmdoctor-shiftleaders",
        ],
        EXPERT: ["cms-dqm-certification-experts", "tkdqmdoctor-experts"],
        ADMIN: ["tkdqmdoctor-admins"],
    }

    extra_data = JSONField(verbose_name="extra data", default=dict)

    user_privilege = models.IntegerField(choices=USER_PRIVILEGE_CHOICES, default=GUEST)

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
                is_staff = True
                logger.info("User {} is now staff".format(self))
                shift_leader_group = get_or_create_shift_leader_group(
                    self.SHIFT_LEADER_GROUP_NAME
                )
                groups.add(shift_leader_group)
                logger.info(
                    "User {} has been added "
                    "to the shift leader group".format(self)
                )

            if self.user_privilege >= self.ADMIN:
                is_superuser = True
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
            or is_staff
            or is_superuser
        )

    @property
    def has_shift_leader_rights(self):
        return (
            self.user_privilege in (self.SHIFTLEADER, self.EXPERT, self.ADMIN)
            or is_staff
            or is_superuser
        )
