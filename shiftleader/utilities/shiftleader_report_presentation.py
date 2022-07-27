"""
OpenDocumentPresentation generator for shiftleader reports
"""
from typing import List as tList
import logging
from datetime import datetime
from django.conf import settings
from certifier.query import TrackerCertificationQuerySet
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
    TableProperties,
)
from odf import dc
from odf.text import P, List, ListItem, ListLevelStyleBullet
from odf.presentation import Header
from odf.draw import Page, Frame, TextBox, Image
from odf.table import Table, TableColumn, TableRow, TableCell
from shiftleader.utilities.shiftleader_report import ShiftLeaderReport


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
        names_shifters: tList[str] = [""],
        names_oncall: tList[str] = [""],
        certification_queryset: TrackerCertificationQuerySet = None,
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
        self.queryset = certification_queryset
        logger.debug(
            f"TrackerCertification queryset contains {self.queryset.count()} objects"
        )
        self.doc = OpenDocumentPresentation()

        self._configure_styles()

        # Do some heavy lifting
        self.slreport = ShiftLeaderReport(self.queryset)

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
        self.titlestyle = Style(name="TitleOnly-title", family="presentation")
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
            name="TitleAndContent-title", family="presentation"
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

        self.textstyle_content = Style(
            name="TitleAndContent-subtitle", family="presentation"
        )
        self.textstyle_content.addElement(
            ParagraphProperties(textalign="left", verticalalign="middle")
        )
        self.textstyle_content.addElement(
            TextProperties(fontsize="12pt", fontfamily="sans", color="#000000")
        )
        self.textstyle_content.addElement(
            GraphicProperties(
                fillcolor="#ffffff", strokecolor="#ffffff", overflowbehavior="clip"
            )
        )
        self.doc.styles.addElement(self.textstyle_content)

        # Style for adding content
        self.subtitlestyle = Style(name="TitleOnly-subtitle", family="presentation")
        self.subtitlestyle.addElement(ParagraphProperties(textalign="center"))
        self.subtitlestyle.addElement(
            TextProperties(fontsize="32pt", fontfamily="sans", color="#8b8b8b")
        )
        self.subtitlestyle.addElement(
            GraphicProperties(fillcolor="#ffffff", strokecolor="#ffffff")
        )
        self.doc.styles.addElement(self.subtitlestyle)

        # Style for images
        # self.photostyle = Style(name="TitleOnly-photo", family="presentation")
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
        self.masterpage = MasterPage(name="TitleOnly", pagelayoutname=pagelayout)
        self.doc.masterstyles.addElement(self.masterpage)

        self.masterpagecontent = MasterPage(
            name="TitleAndContent", pagelayoutname=pagelayout
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

    def _generate_list(self, list_items: list) -> List:
        l = List()
        for item in list_items:
            li = ListItem()
            li.addElement(P(text=item))
            l.addElement(li)
        return l

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
        if not self.queryset.run_numbers():
            logger.debug("No runs certified")
            return

        # Sample data for testing
        fills = [
            {"fill_number": 7963, "certified_runs": [355407]},
            {"fill_number": 7963, "certified_runs": [355407]},
            {"fill_number": 7963, "certified_runs": [355407]},
            {"fill_number": 7963, "certified_runs": [355407]},
            {
                "fill_number": 7963,
                "certified_runs": [355407, 355407, 355407, 355407],
            },
        ]
        table_names = {
            "Collisions Express": {"fills": fills},
            "Collisions Prompt": {"fills": fills},
            "Cosmics Express": {"fills": fills},
            "Cosmics Prompt": {"fills": fills},
        }

        # logger.debug("Getting information on collisions express")
        # collisions_express = self.slreport.collisions().express().fills()
        # logger.debug("Getting information on collisions prompt")
        # collisions_prompt = self.slreport.collisions().prompt().fills()
        # logger.debug("Getting information on cosmics express")
        # cosmics_express = self.slreport.cosmics().express().fills()
        # logger.debug("Getting information on cocmics prompt")
        # cosmics_prompt = self.slreport.cosmics().prompt().fills()
        # table_names = {
        #     "Collisions Express": {"fills": collisions_express},
        #     "Collisions Prompt": {"fills": collisions_prompt},
        #     "Cosmics Express": {"fills": cosmics_express},
        #     "Cosmics Prompt": {"fills": cosmics_prompt},
        # }
        # logger.debug("Done.")

        # Iterate over all required tables
        for table_name, table_config in table_names.items():
            logger.debug(f"Creating table {table_name}")
            page = self._create_content_page(title=f"List of LHC Fills - {table_name}")

            # Frame style
            self.frametablestyle = Style(name="TitleOnly-table", family="presentation")
            self.frametablestyle.addElement(
                ParagraphProperties(textalign="left", verticalalign="middle")
            )
            self.frametablestyle.addElement(TextProperties(fontfamily="sans"))
            self.frametablestyle.addElement(
                TableProperties(
                    backgroundcolor="#ffffff",
                )
            )
            self.doc.styles.addElement(self.frametablestyle)

            table_frame = Frame(
                stylename=self.frametablestyle,
                width="648pt",
                height="105pt",
                x="40pt",
                y="117pt",
            )

            table = self._create_table()
            tablecontents = Style(name="Table Contents", family="paragraph")
            tablecontents.addElement(
                ParagraphProperties(numberlines="false", linenumber="0")
            )

            # tablecontents.addElement(GraphicProperties())
            self.doc.styles.addElement(tablecontents)

            # Two columns
            table.addElement(TableColumn())
            table.addElement(TableColumn())

            # Header
            tr = TableRow()
            table.addElement(tr)
            for col_name in ["Fill Number", "Certified Runs"]:
                tc = TableCell()
                tc.addElement(P(text=col_name, stylename=tablecontents))
                tr.addElement(tc)

            # Add fill information
            for fill in table_config["fills"]:
                tr = TableRow()
                table.addElement(tr)
                # keys: fill_number, certified_runs
                for k, v in fill.items():
                    tc = TableCell()
                    tr.addElement(tc)
                    tc.addElement(P(text=v, stylename=tablecontents))

            table_frame.addElement(table)
            page.addElement(table_frame)

    def _add_page_day_by_day(self):
        for day in self.slreport.day_by_day():
            page = self._create_content_page(
                title=f"Day by day notes: {day.name()}, {day.date()}"
            )
            frame = self._create_full_page_content_frame()
            tb = TextBox()
            tb.addElement(P(text="TESTT"))
            tb.addElement(self._generate_list(["asdfasd", "sadfsadf"]))
            frame.addElement(tb)
            page.addElement(frame)

    def _add_page_summary(self):
        page = self._create_content_page(title=f"Summary of week {self.week_number}")
        # TODO: add content

    def _add_page_list_express(self):
        page = self._create_content_page(title="List of runs certified PromptReco")
        # TODO: add content

    def _add_page_list_prompt(self):
        page = self._create_content_page(title="List of runs certified StreamExpress")
        # TODO: add content

    def _create_full_page_content_frame(self):
        return Frame(
            stylename=self.textstyle_content,
            width="648pt",
            height=f"410pt",
            x="36pt",
            y="110pt",
        )

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

    def _create_table(self):
        table = Table()
        return table

    def save(self, filename: str = "") -> None:
        if not filename or filename == "":
            filename = self._generate_filename()
        self.doc.save(outputfile=filename)