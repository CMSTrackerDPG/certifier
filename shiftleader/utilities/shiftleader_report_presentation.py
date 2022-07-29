"""
OpenDocumentPresentation generator for shiftleader reports
"""
from typing import List as tList
import logging
from datetime import datetime, date, timedelta
from django.conf import settings
from certifier.models import TrackerCertification
from shiftleader.utilities.shiftleader_report import ShiftLeaderReport
from shiftleader.templatetags.shiftleaderfilters import join_good_runs
from listruns.utilities.luminosity import format_integrated_luminosity
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
    ListLevelProperties,
    TableCellProperties,
    TableColumnProperties,
    TableRowProperties,
)
from odf import dc
from odf.text import (
    P,
    List,
    ListItem,
    ListLevelStyleBullet,
    ListStyle,
    Span,
    PageNumber,
)
from odf.draw import Page, Frame, TextBox
from odf.table import Table, TableColumn, TableRow, TableCell


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
        # certification_queryset: TrackerCertificationQuerySet = None,
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

        # Get first day of week requested
        week_start = date.fromisocalendar(year=year, week=week_number, day=1)

        week_end = week_start + timedelta(days=6)

        queryset = TrackerCertification.objects.filter(
            date__gte=week_start,
            date__lte=week_end,
        )

        self.queryset = queryset
        logger.debug(
            f"TrackerCertification queryset contains {self.queryset.count()} objects"
        )
        self.doc = OpenDocumentPresentation()

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

        # Styles
        self._configure_styles()

        # Create a shiftleader report instance
        self.slreport = ShiftLeaderReport(self.queryset)

        # Add pages
        self._add_page_title()
        self._add_page_recorded_luminosity()
        self._add_page_list_lhc_fills()
        self._add_page_day_by_day()
        self._add_page_weekly_certification()
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
        self.titlestyle.addElement(GraphicProperties(fill="none", stroke="none"))
        self.doc.styles.addElement(self.titlestyle)

        # Style for Frame which has a title in it
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
            GraphicProperties(fill="none", stroke="none", overflowbehavior="clip")
        )
        self.doc.styles.addElement(self.titlestyle_content)

        # Style for frame which has a subtitle in it (used in content pages)
        self.style_content_subtitle = Style(
            name="TitleAndContent-subtitle", family="presentation"
        )
        self.style_content_subtitle.addElement(
            ParagraphProperties(textalign="left", verticalalign="middle")
        )
        self.style_content_subtitle.addElement(
            TextProperties(fontsize="12pt", fontfamily="sans", color="#000000")
        )
        self.style_content_subtitle.addElement(
            GraphicProperties(fill="none", stroke="none", overflowbehavior="clip")
        )
        self.doc.styles.addElement(self.style_content_subtitle)

        # Style for frame which has a subtitle in it (used in main title page)
        self.subtitlestyle = Style(name="TitleOnly-subtitle", family="presentation")
        self.subtitlestyle.addElement(ParagraphProperties(textalign="center"))
        self.subtitlestyle.addElement(
            TextProperties(fontsize="32pt", fontfamily="sans", color="#8b8b8b")
        )
        self.subtitlestyle.addElement(GraphicProperties(fill="none", stroke="none"))
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
                displayfooter="true",
                displaypagenumber="true",
            )
        )
        self.doc.automaticstyles.addElement(self.dpstyle)

        # Every drawing page must have a master page assigned to it.
        # Master page for title-only slide
        self.masterpage = MasterPage(name="TitleOnly", pagelayoutname=pagelayout)
        self.doc.masterstyles.addElement(self.masterpage)

        # Master page for content pages
        self.masterpagecontent = MasterPage(
            name="TitleAndContent", pagelayoutname=pagelayout
        )
        self.doc.masterstyles.addElement(self.masterpagecontent)

        # Table cell style
        self.style_cell = Style(name="ce1", family="table-cell")
        self.style_cell.addElement(
            GraphicProperties(
                fillcolor="#ffffff",
                textareaverticalalign="middle",
            )
        )
        self.style_cell.addElement(
            TableCellProperties(
                paddingtop="0.1in",
                paddingleft="0.1in",
                paddingright="0.1in",
                paddingbottom="0.1in",
                backgroundcolor="#ffffff",
            )
        )
        self.style_cell.addElement(
            ParagraphProperties(
                border="0.03pt solid #000000", writingmode="lr-tb", textalign="left"
            )
        )
        self.doc.automaticstyles.addElement(self.style_cell)

        # Header Cell style
        self.style_cell_header = Style(name="ceh", family="table-cell")
        self.style_cell_header.addElement(
            GraphicProperties(fillcolor="#dddddd", textareaverticalalign="middle")
        )
        self.style_cell_header.addElement(
            ParagraphProperties(
                border="0.03pt solid #000000", writingmode="lr-tb", textalign="left"
            )
        )

        self.style_cell_header.addElement(
            TableCellProperties(
                paddingtop="0.1in",
                paddingleft="0.1in",
                paddingright="0.1in",
                paddingbottom="0.1in",
                backgroundcolor="#dddddd",
            )
        )
        self.doc.automaticstyles.addElement(self.style_cell_header)

        # List style L1-1
        self.list_style_l1 = ListStyle(name="L1-1")
        list_level_style_bullet = ListLevelStyleBullet(level="1", bulletchar="●")
        list_level_style_bullet.addElement(
            ListLevelProperties(spacebefore="0.3cm", minlabelwidth="0.9cm")
        )
        list_level_style_bullet.addElement(
            TextProperties(
                fontfamily="StarSymbol", usewindowfontcolor="true", fontsize="60%"
            )
        )

        self.list_style_l1.addElement(list_level_style_bullet)
        self.doc.automaticstyles.addElement(self.list_style_l1)

        # List style L2
        self.list_style_l2 = ListStyle(name="L1-2")
        list_level_style_bullet = ListLevelStyleBullet(level="2", bulletchar="⃝")
        list_level_style_bullet.addElement(
            ListLevelProperties(spacebefore="1.5cm", minlabelwidth="0.9cm")
        )
        list_level_style_bullet.addElement(
            TextProperties(
                fontfamily="StarSymbol", usewindowfontcolor="true", fontsize="45%"
            )
        )

        self.list_style_l2.addElement(list_level_style_bullet)
        self.doc.automaticstyles.addElement(self.list_style_l2)

        # List style L3
        self.list_style_l3 = ListStyle(name="L1-3")
        list_level_style_bullet = ListLevelStyleBullet(level="3", bulletchar="■")
        list_level_style_bullet.addElement(
            ListLevelProperties(spacebefore="3.3cm", minlabelwidth="0.9cm")
        )
        list_level_style_bullet.addElement(
            TextProperties(
                fontfamily="StarSymbol", usewindowfontcolor="true", fontsize="60%"
            )
        )

        self.list_style_l3.addElement(list_level_style_bullet)
        self.doc.automaticstyles.addElement(self.list_style_l3)

        # Style for frame which has list in it (??)
        self.style_frame_list = Style(
            name="pr1", family="presentation", liststylename=self.list_style_l1
        )
        self.style_frame_list.addElement(
            GraphicProperties(
                stroke="none",
                fill="none",
                textareaverticalalign="top",
                fittosize="shrink-to-fit",
                shrinktofit="true",
                paddingtop="0.127cm",
                paddingbottom="0.127cm",
            )
        )
        self.doc.automaticstyles.addElement(self.style_frame_list)

        # Span for tables
        self.style_span = Style(name="sp1", family="text")
        self.style_span.addElement(TextProperties(fontfamily="sans"))
        self.doc.automaticstyles.addElement(self.style_span)

        self.style_span_header = Style(name="sph", family="text")
        self.style_span_header.addElement(
            TextProperties(
                fontfamily="sans",
                fontweight="bold",
                fontweightasian="bold",
                fontweightcomplex="bold",
            )
        )
        self.doc.automaticstyles.addElement(self.style_span_header)

        # Paragraph for pagenumber
        self.style_p_pagenumber = Style(name="ppn", family="paragraph")
        self.style_p_pagenumber.addElement(ParagraphProperties(textalign="end"))
        self.style_p_pagenumber.addElement(
            GraphicProperties(
                stroke="none",
                fill="none",
            )
        )
        self.doc.automaticstyles.addElement(self.style_p_pagenumber)

        # Span for pagenumber
        self.style_span_pagenumber = Style(name="sppn", family="text")
        self.style_span_pagenumber.addElement(
            TextProperties(
                fontsize="12pt",
                fontsizeasian="12pt",
                fontsizecomplex="1pt",
                fontfamily="sans",
            )
        )
        self.doc.automaticstyles.addElement(self.style_span_pagenumber)

    def _generate_list(self, list_items: list, identation_level: int = 1) -> List:
        stylename = f"L1-{identation_level}"
        l = List(stylename=stylename)
        for item in list_items:
            li = ListItem()

            if isinstance(item, list):
                item = self._generate_list(item, identation_level + 1)
                li.addElement(item)
            else:
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
        """
        LHC fills only
        """
        if not self.queryset.run_numbers():
            logger.debug("No runs certified")
            return

        logger.debug("Getting information on collisions express")
        collisions_express = self.slreport.collisions().express().fills()
        logger.debug("Getting information on collisions prompt")
        collisions_prompt = self.slreport.collisions().prompt().fills()
        logger.debug("Getting information on cosmics express")
        cosmics_express = self.slreport.cosmics().express().fills()
        logger.debug("Getting information on cocmics prompt")
        cosmics_prompt = self.slreport.cosmics().prompt().fills()
        table_names = {
            "Collisions Express": {"fills": collisions_express},
            "Collisions Prompt": {"fills": collisions_prompt},
            "Cosmics Express": {"fills": cosmics_express},
            "Cosmics Prompt": {"fills": cosmics_prompt},
        }
        logger.debug("Done.")

        # Iterate over all required tables
        for table_name, table_config in table_names.items():
            logger.debug(f"Creating table {table_name}")
            page = self._create_content_page(title=f"List of LHC Fills - {table_name}")

            WIDTH_FRAME = 648
            WIDTH_COL = 300
            HEIGHT_FRAME = 105
            HEIGHT_ROW = 50

            table_frame = Frame(
                width=f"{WIDTH_FRAME}pt",
                height=f"{HEIGHT_FRAME}pt",
                x="40pt",
                y="117pt",
            )

            table = self._create_table()

            # Style for rows
            style_row = Style(name="roh", family="table-row")
            style_row.addElement(TableRowProperties(rowheight=f"{HEIGHT_ROW}pt"))
            self.doc.automaticstyles.addElement(style_row)

            # Header row
            tr = TableRow(
                defaultcellstylename=self.style_cell_header, stylename=style_row
            )
            # Two columns
            for i, col_name in enumerate(["Fill Number", "Certified Runs"]):
                style_column = Style(name=f"co{i}", family="table-column")
                style_column.addElement(
                    TableColumnProperties(columnwidth=f"{WIDTH_COL}pt")
                )
                self.doc.automaticstyles.addElement(style_column)

                table.addElement(
                    TableColumn(stylename=style_column, defaultcellstylename="")
                )

                tc = TableCell()
                p = P()
                p.addElement(Span(text=col_name, stylename=self.style_span_header))
                tc.addElement(p)
                tr.addElement(tc)

            table.addElement(tr)

            # Add fill information
            for fill in table_config["fills"]:

                tr = TableRow(defaultcellstylename=self.style_cell, stylename=style_row)
                table.addElement(tr)
                # keys: fill_number, certified_runs
                for k, v in fill.items():
                    tc = TableCell()
                    tr.addElement(tc)
                    p = P()
                    p.addElement(Span(text=v, stylename=self.style_span))
                    tc.addElement(p)

            table_frame.addElement(table)
            page.addElement(table_frame)

    def _add_page_day_by_day(self):
        """
        Day-by-day certification report
        """
        for day in self.slreport.day_by_day():
            page = self._create_content_page(
                title=f"Day by day notes: {day.name()}, {day.date()}"
            )
            frame = self._create_full_page_content_frame(self.style_frame_list)
            tb = TextBox()
            list1 = self._generate_list(
                list_items=[
                    f"Fills {str(day.collisions().express().fill_numbers())}",
                    [
                        "[insert here] colliding bunches, peak lumi [insert here] x 10³³ cm²/s",
                    ],
                    "Number of runs certified:",
                    [
                        f"Collisions: {day.collisions().express().total_number()} in Stream-Express ({format_integrated_luminosity(day.collisions().express().integrated_luminosity())}), {day.collisions().prompt().total_number()} in Prompt-Reco ({format_integrated_luminosity(day.collisions().prompt().integrated_luminosity())})",
                        f"Cosmics: {day.cosmics().express().total_number()} in Stream-Express, {day.cosmics().prompt().total_number()} in Prompt-Reco",
                    ],
                    f"Total number of BAD runs = {day.bad().total_number()} ({format_integrated_luminosity(day.bad().integrated_luminosity())})",
                    [
                        f"Number of changed flags from Express to Prompt={day.flag_changed().total_number()}"
                        + f" ({day.flag_changed().good().run_numbers()})"  # TODO, format as green?
                        if day.flag_changed().total_number() > 0
                        else ""
                    ],
                    "Conditions update:",
                    "Issues reported in the Elog and feedback to Online:",
                    "On calls:",
                ]
            )
            tb.addElement(list1)
            tb.addElement(P(text="Daily Shifter Summaries:"))
            tb.addElement(P(text="Prompt Feedback plots:"))

            frame.addElement(tb)
            page.addElement(frame)

    def _add_page_weekly_certification(self):
        """
        Weekly certification page
        """
        page = self._create_content_page(title=f"Weekly certification")
        frame = self._create_full_page_content_frame(self.style_frame_list)
        tb = TextBox()
        list1 = self._generate_list(
            list_items=[
                "Collisions",
                [
                    f"Prompt-Reco: total number={self.slreport.collisions().prompt().total_number()}, Integrated lumi={format_integrated_luminosity(self.slreport.collisions().prompt().integrated_luminosity())}",
                    [
                        f"BAD runs: total number={self.slreport.bad().collisions().prompt().total_number()}, Integrated luminosity={format_integrated_luminosity(self.slreport.bad().collisions().prompt().integrated_luminosity())}"
                    ],
                    f"Stream-Express: total number={self.slreport.collisions().express().total_number()}, Integrated lumi={format_integrated_luminosity(self.slreport.collisions().express().integrated_luminosity())}",
                    [
                        f"BAD runs: total number={self.slreport.bad().collisions().express().total_number()}, Integrated luminosity={format_integrated_luminosity(self.slreport.bad().collisions().express().integrated_luminosity())}"
                    ],
                ],
                "Cosmics",
                [
                    f"Prompt-Reco: total number={self.slreport.cosmics().prompt().total_number()}",
                    [
                        f"BAD runs: total number={self.slreport.bad().cosmics().prompt().total_number()}"
                    ],
                    f"Stream-Express: total number={self.slreport.cosmics().express().total_number()}",
                    [
                        f"BAD runs: total number={self.slreport.bad().cosmics().express().total_number()}"
                    ],
                ],
                "Central certification:",
                ["list of runs:", "deadline has been met?"],
            ]
        )
        tb.addElement(list1)
        frame.addElement(tb)
        page.addElement(frame)

    def _add_page_summary(self):
        page = self._create_content_page(title=f"Summary of week {self.week_number}")
        # TODO: add content

    def _add_page_list_express(self):
        page = self._create_content_page(title="List of runs certified StreamExpress")
        frame = self._create_full_page_content_frame(self.style_frame_list)
        tb = TextBox()
        list1 = self._generate_list(
            list_items=[
                "Collisions",
                [
                    f"{day.name()}: Good: {[run_number for run_number in day.good().run_numbers()]}, "
                    + (
                        f"Bad: {[run_number for run_number in day.bad().run_numbers()]}"
                        if len(day.bad().run_numbers()) > 0
                        else ""
                    )
                    for day in self.slreport.collisions().express().day_by_day()
                ],
                "Cosmics",
                [
                    f"{day.name()}: Good: {[run_number for run_number in day.good().run_numbers()]}, "
                    + (
                        f"Bad: {[run_number for run_number in day.bad().run_numbers()]}"
                        if len(day.bad().run_numbers()) > 0
                        else ""
                    )
                    for day in self.slreport.cosmics().express().day_by_day()
                ],
            ]
        )
        tb.addElement(list1)
        frame.addElement(tb)
        page.addElement(frame)

    def _add_page_list_prompt(self):
        page = self._create_content_page(title="List of runs certified Prompt")
        frame = self._create_full_page_content_frame(self.style_frame_list)
        tb = TextBox()
        list1 = self._generate_list(
            list_items=[
                "Collisions",
                [
                    f"{day.name()}: Good: {[run_number for run_number in day.good().run_numbers()]}, "
                    + (
                        f"Bad: {[run_number for run_number in day.bad().run_numbers()]}"
                        if len(day.bad().run_numbers()) > 0
                        else ""
                    )
                    for day in self.slreport.collisions().prompt().day_by_day()
                ],
                "Cosmics",
                [
                    f"{day.name()}: Good: {[run_number for run_number in day.good().run_numbers()]}, "
                    + (
                        f"Bad: {[run_number for run_number in day.bad().run_numbers()]}"
                        if len(day.bad().run_numbers()) > 0
                        else ""
                    )
                    for day in self.slreport.cosmics().prompt().day_by_day()
                ],
            ]
        )
        tb.addElement(list1)
        frame.addElement(tb)
        page.addElement(frame)

    def _create_full_page_content_frame(self, stylename: str = None):
        """
        Helper method to create a generic frame with appropriate
        dimensions, suitable for this document's size.

        A stylename can be given, or the default style_content_subtitle
        is used.
        """
        return Frame(
            stylename=stylename if stylename else self.style_content_subtitle,
            width="648pt",
            height="410pt",
            x="36pt",
            y="110pt",
        )

    def _create_content_page(self, title: str):
        """
        Generic content page skeleton generator.
        Creates a page, adds a title and returns the
        created page.
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

        frame_pagenumber = Frame(
            width="81.1pt", height="26.5pt", x="639.6pt", y="506.3pt"
        )

        textbox = TextBox()
        p = P(stylename=self.style_p_pagenumber)
        span = Span(stylename=self.style_span_pagenumber)
        span.addElement(PageNumber())
        p.addElement(span)
        textbox.addElement(p)
        frame_pagenumber.addElement(textbox)
        page.addElement(frame_pagenumber)
        return page

    def _create_table(self):
        table = Table()
        return table

    def save(self, filename: str = "") -> None:
        if not filename or filename == "":
            filename = self._generate_filename()
        try:
            self.doc.save(outputfile=filename)
            logger.info(f"Presentation saved at '{filename}'!")
        except Exception as e:
            logger.exception(repr(e))
