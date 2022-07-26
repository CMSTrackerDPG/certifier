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
        self.requesting_user = requesting_user
        self.certhelper_version = certhelper_version
        self.name_shift_leader = name_shift_leader
        self.names_shifters = names_shifters
        self.names_oncall = names_oncall

        self.doc = OpenDocumentPresentation()

        self._configure_styles()

        # Add pages
        self._add_page_title()
        self._add_page_recorded_luminosity()
        self._add_page_list_lhc_fills()
        self._add_page_day_by_day()
        self._add_page_summary()
        self._add_page_list_express()
        self._add_page_list_prompt()

    def _configure_styles(self):
        pagelayout = PageLayout(name="MyLayout")
        self.doc.automaticstyles.addElement(pagelayout)
        pagelayout.addElement(
            PageLayoutProperties(
                margin="0cm",
                pagewidth="720pt",
                pageheight="540pt",
                printorientation="landscape",
            )
        )

        # Style for page titles
        # The name attribute *must* start with the name of the masterpage
        # The name after the dash *also* matters (should be "title", "subtitle"
        # or "photo").
        self.titlestyle = Style(name="MyMaster-title", family="presentation")
        self.titlestyle.addElement(
            ParagraphProperties(textalign="center", verticalalign="middle")
        )
        self.titlestyle.addElement(TextProperties(fontsize="44pt", fontfamily="sans"))
        self.titlestyle.addElement(
            GraphicProperties(fillcolor="#ffffff", strokecolor="#ffffff")
        )
        self.doc.styles.addElement(self.titlestyle)

        # Different style for content titles
        self.titlestyle_content = Style(
            name="MyMasterContent-title", family="presentation"
        )
        self.titlestyle_content.addElement(
            ParagraphProperties(textalign="center", verticalalign="middle")
        )
        self.titlestyle_content.addElement(
            TextProperties(fontsize="44pt", fontfamily="sans", color="#00b0f0")
        )
        self.titlestyle_content.addElement(
            GraphicProperties(
                fillcolor="#ffffff", strokecolor="#ffffff", overflowbehavior="clip"
            )
        )
        self.doc.styles.addElement(self.titlestyle_content)

        # Style for adding content
        self.subtitlestyle = Style(name="MyMaster-subtitle", family="presentation")
        self.subtitlestyle.addElement(ParagraphProperties(textalign="center"))
        self.subtitlestyle.addElement(
            TextProperties(fontsize="32pt", fontfamily="sans", color="#8b8b8b")
        )
        self.subtitlestyle.addElement(
            GraphicProperties(fillcolor="#ffffff", strokecolor="#ffffff")
        )
        self.doc.styles.addElement(self.subtitlestyle)

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

        self.masterpagecontent = MasterPage(
            name="MyMasterContent", pagelayoutname=pagelayout
        )
        self.doc.masterstyles.addElement(self.masterpagecontent)

        # Metadata
        self.doc.meta.addElement(
            dc.Title(text=f"Shiftleader Report for {self.year} week {self.week_number}")
        )
        self.doc.meta.addElement(dc.Date(text=datetime.now().isoformat()))
        # self.doc.meta.addElement(dc.Subject(text="Shiftleader Report"))
        self.doc.meta.addElement(
            dc.Creator(
                text=f"CertHelper version {self.certhelper_version}, requested by {self.requesting_user}"
            )
        )

    def _generate_filename(self) -> str:
        return f"shiftleader_report_{self.year}_week_{self.week_number}.odp"

    def _add_page_title(self):
        """
        Add title page to presentation
        """
        page = Page(stylename=self.dpstyle, masterpagename=self.masterpage)
        self.doc.presentation.addElement(page)
        titleframe = Frame(
            stylename=self.titlestyle,
            width="612pt",
            height="115.7pt",
            x="54pt",
            y="167.8pt",
        )
        textbox = TextBox()
        titleframe.addElement(textbox)
        textbox.addElement(P(text="Offline Shift Leader Report"))
        textbox.addElement(P(text=f"Week {self.week_number}"))
        page.addElement(titleframe)

        c_frame = Frame(
            stylename=self.subtitlestyle,
            width="633.6pt",
            height="138pt",
            x="43.2pt",
            y="306pt",
        )
        c_text = TextBox()
        c_frame.addElement(c_text)
        c_text.addElement(P(text=f"SL: {self.name_shift_leader}"))
        c_text.addElement(
            P(
                text=f"""Shifters: {str(self.names_shifters).replace('[', '').replace(']', '').replace("'", '')}"""
            )
        )
        c_text.addElement(
            P(
                text=f"""On-call: {str(self.names_oncall).replace('[', '').replace(']', '').replace("'", '')}"""
            )
        )
        page.addElement(c_frame)

    def _add_page_recorded_luminosity(self):
        page = self._create_content_page(title="Recorded Luminosity")
        # TODO: add content

    def _add_page_list_lhc_fills(self):
        page = self._create_content_page(title="List of LHC Fills")
        # TODO: add content

    def _add_page_day_by_day(self):
        days = []
        for day in days:
            page = self._create_content_page(title=f"Day by day notes: {day}")
            # TODO: add content

    def _add_page_summary(self):
        page = self._create_content_page(title=f"Summary of week {self.week_number}")
        # TODO: add content

    def _add_page_list_express(self):
        page = self._create_content_page(title="List of runs certified PromptReco")
        # TODO: add content

    def _add_page_list_prompt(self):
        page = self._create_content_page(title="List of runs certified StreamExpress")
        # TODO: add content

    def _create_content_page(self, title: str):
        """
        Generic content page skeleton generator.
        Only adds title.
        """
        page = Page(stylename=self.dpstyle, masterpagename=self.masterpagecontent)
        self.doc.presentation.addElement(page)

        titleframe = Frame(
            stylename=self.titlestyle_content,
            width="648pt",
            height="90pt",
            x="36pt",
            y="3.5pt",
        )
        textbox = TextBox()
        titleframe.addElement(textbox)
        textbox.addElement(P(text=title))
        page.addElement(titleframe)
        return page

    def save(self, filename: str = "") -> None:
        if not filename or filename == "":
            filename = self._generate_filename()
        self.doc.save(outputfile=filename)
