"""
OpenDocumentPresentation generator for shiftleader reports
"""
from typing import List
import logging
from datetime import datetime
from django.conf import settings
from odf.opendocument import OpenDocumentPresentation
from odf.style import (
    Style,
    MasterPage,
    PageLayout,
    PageLayoutProperties,
    TextProperties,
    GraphicProperties,
    ParagraphProperties,
    DrawingPageProperties,
)
from odf import dc
from odf.text import P
from odf.presentation import Header
from odf.draw import Page, Frame, TextBox, Image


logger = logging.getLogger(__name__)


class ShiftLeaderReportPresentation(object):
    """
    ODF Presentation generator for Shiftleader Reports.

    - Title page
    - Recorded Luminosity
    - List of LHC Fills
    - Day by day notes
    - Week summary
    - Weekly certification
    """

    def __init__(
        self,
        requesting_user: str = "",
        certhelper_version: str = settings.CERTHELPER_VERSION,
        week_number: str = "",
        year: int = datetime.now().year,
        name_shift_leader: str = "",
        names_shifters: List[str] = [""],
        names_oncall: List[str] = [""],
    ):
        logger.info(
            f"ShiftLeader presentation generation for week {week_number} requested by {requesting_user}"
        )

        self.week_number = week_number
        self.year = year
        self.name_shift_leader = name_shift_leader
        self.names_shifters = names_shifters
        self.names_oncall = names_oncall

        self.doc = OpenDocumentPresentation()

        pagelayout = PageLayout(name="MyLayout")
        self.doc.automaticstyles.addElement(pagelayout)
        pagelayout.addElement(
            PageLayoutProperties(
                margin="0cm",
                pagewidth="28cm",
                pageheight="21cm",
                printorientation="landscape",
            )
        )

        # Style for page titles
        # The name attribute *must* start with the name of the masterpage
        # The name after the dash *also* matters (should be "title", "subtitle"
        # or "photo").
        self.titlestyle = Style(name="MyMaster-title", family="presentation")
        self.titlestyle.addElement(ParagraphProperties(textalign="center"))
        self.titlestyle.addElement(TextProperties(fontsize="30pt", fontfamily="sans"))
        self.titlestyle.addElement(
            GraphicProperties(fillcolor="#ffffff", strokecolor="#ffffff")
        )
        self.doc.styles.addElement(self.titlestyle)

        # Style for adding content
        self.teststyle = Style(name="MyMaster-subtitle", family="presentation")
        self.teststyle.addElement(ParagraphProperties(textalign="left"))
        self.teststyle.addElement(TextProperties(fontsize="14pt", fontfamily="sans"))
        self.teststyle.addElement(
            GraphicProperties(fillcolor="#ffffff", strokecolor="#ffffff")
        )
        self.doc.styles.addElement(self.teststyle)

        # Style for images
        # self.photostyle = Style(name="MyMaster-photo", family="presentation")
        # self.doc.styles.addElement(self.photostyle)

        # Style for pages and transitions
        self.dpstyle = Style(name="dp1", family="drawing-page")
        self.dpstyle.addElement(
            DrawingPageProperties(
                transitiontype="none",
                # transitionstyle="move-from-top",
                duration="PT00S",
            )
        )
        self.doc.automaticstyles.addElement(self.dpstyle)

        # Every drawing page must have a master page assigned to it.
        self.masterpage = MasterPage(name="MyMaster", pagelayoutname=pagelayout)
        self.doc.masterstyles.addElement(self.masterpage)

        # Metadata
        self.doc.meta.addElement(
            dc.Title(text="Shiftleader Report for {self.year} week {self.week}")
        )
        self.doc.meta.addElement(dc.Date(text=datetime.now().isoformat()))
        # self.doc.meta.addElement(dc.Subject(text="Shiftleader Report"))
        self.doc.meta.addElement(
            dc.Creator(
                text=f"CertHelper version {certhelper_version}, requested by {requesting_user}"
            )
        )

    def _generate_filename(self) -> str:
        return f"shiftleader_report_{self.year}_week_{self.week_number}.odp"

    def save(self, filename: str = "") -> None:
        if not filename or filename == "":
            filename = self._generate_filename()
        self.doc.save(outputfile=filename)
