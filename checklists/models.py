from django.db import models

from ckeditor.fields import RichTextField

# Create your models here.

class Checklist(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = RichTextField(
        blank=True,
        help_text="Text that will be displayed above the checklist items to provide "
        "further information needed to the explain the problems",
    )

    additional_description = RichTextField(
        blank=True,
        help_text="Text that will be displayed under the checklist items to provide "
        "tips and links",
    )

    "identifier can be used to check via javascript if checkbox has been ticked "
    "and to pop up a modal related to the checklist"
    identifier = models.SlugField(
        unique=True,
        max_length=15,
        help_text="Short unique word used to identify the checklist in the website. "
        "Examples: general, trackermap, pixel, sistrip, tracking",
    )

    def __str__(self):
        return self.title


class ChecklistItemGroup(models.Model):
    """
    Groups a bunch of Checklist Items together
    E.g. one group for tips and one for general checks
    """

    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Used as a Subheadline to group bullet points together",
    )

    description = RichTextField(
        blank=True,
        help_text="Text that will be displayed above the checklist items to provide"
        "further information needed to the explain the problems",
    )


class ChecklistItem(models.Model):
    checklistgroup = models.ForeignKey(ChecklistItemGroup, on_delete=models.CASCADE)
    text = RichTextField(help_text="Text that will be displayed at the bullet point")

    def __str__(self):
        return self.text
