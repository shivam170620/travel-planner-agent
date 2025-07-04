from typing import Dict, Any, List
from utils.llm_wrapper.llms import llm
from utils.config import FINAL_REPORT_GENERATION_PROMPT
from langchain_core.prompts import PromptTemplate
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from datetime import datetime
import os
import re


class ReportGenerator:
    def __init__(
        self,
        origin_city: str,
        destination_city: str,
        num_days: int,
        flight_info: Dict[str, Any],
        weather_info: Dict[str, Any],
        attraction_info: List[Dict[str, Any]],
        restaurant_info: List[Dict[str, Any]],
        hotel_info: List[Dict[str, Any]],
        transport_info: Dict[str, Any],
        expense_report_text: str,
        outbound_date: str = "",
        return_date: str = "",
        output_dir: str = "generated_reports",
    ):
        self.origin_city = origin_city
        self.destination_city = destination_city
        self.num_days = num_days
        self.flight_info = flight_info
        self.weather_info = weather_info
        self.attraction_info = attraction_info
        self.restaurant_info = restaurant_info
        self.hotel_info = hotel_info
        self.transport_info = transport_info
        self.expense_report_text = expense_report_text
        self.output_dir = output_dir
        self.currency = "INR"  # Default currency, can be modified if needed
        self.outbound_date = outbound_date
        self.return_date = return_date
        self.final_report = ""

    def generate_prompt(self) -> str:
        prompt = PromptTemplate.from_template(FINAL_REPORT_GENERATION_PROMPT)
        return prompt.format(
            origin_city=self.origin_city,
            destination_city=self.destination_city,
            num_days=self.num_days,
            flight_info=json.dumps(self.flight_info, indent=2),
            weather_info=json.dumps(self.weather_info, indent=2),
            attraction_info=json.dumps(self.attraction_info, indent=2),
            restaurant_info=json.dumps(self.restaurant_info, indent=2),
            hotel_info=json.dumps(self.hotel_info, indent=2),
            transport_info=json.dumps(self.transport_info, indent=2),
            currency=self.currency,
            expense_report_text=self.expense_report_text,
            outbound_date=self.outbound_date,
            return_date=self.return_date
        )

    def call_llm(self, prompt: str) -> str:
        response = llm.invoke(prompt)
        return response.content.strip() if isinstance(response.content, str) else "Failed to generate report."

    def save_pdf(self, report_text: str, output_dir: str = "generated_reports") -> str:

        # --- Emoji replacement map ---
        emoji_replacements = {
            '✈️': '',
            '🌦️': '',
            '🌧️': '',
            '☀️': '',
            '🏛️': '',
            '🎯': '',
            '📍': '',
            '🕐': '',
            '💰': '',
            '🌡️': '',
            '🎪': '',
            '🏨': '',
            '🍽️': ''
        }

        def replace_emojis(text: str) -> str:
            for emoji, replacement in emoji_replacements.items():
                text = text.replace(emoji, replacement)
            return text

        # File naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.origin_city}_to_{self.destination_city}_{timestamp}.pdf"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        # Setup PDF doc
        doc = SimpleDocTemplate(file_path, pagesize=A4,
                                leftMargin=50, rightMargin=50,
                                topMargin=60, bottomMargin=40)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="CustomHeading1", fontName="Helvetica-Bold", fontSize=16, leading=20,
                                spaceAfter=10, textColor=colors.HexColor("#1F4E79")))
        styles.add(ParagraphStyle(name="CustomHeading2", fontName="Helvetica-Bold", fontSize=13, leading=18,
                                spaceAfter=6, textColor=colors.HexColor("#1F4E79")))
        styles.add(ParagraphStyle(name="CustomBody", fontName="Helvetica", fontSize=11, leading=15))
        styles.add(ParagraphStyle(name="CustomBullet", fontName="Helvetica", fontSize=11, leftIndent=15, bulletIndent=5))

        content = []
        lines = report_text.splitlines()
        bullet_buffer = []

        def flush_bullets():
            nonlocal bullet_buffer
            for line in bullet_buffer:
                content.append(Paragraph(line, styles["CustomBullet"]))
            bullet_buffer = []

        for line in lines:
            line = line.strip()
            if not line:
                flush_bullets()
                content.append(Spacer(1, 10))
                continue

            if line.startswith("# "):
                flush_bullets()
                content.append(Paragraph(replace_emojis(line[2:]), styles["CustomHeading1"]))

            elif line.startswith("## "):
                flush_bullets()
                content.append(Paragraph(replace_emojis(line[3:]), styles["CustomHeading2"]))

            elif line.startswith("### "):
                flush_bullets()
                content.append(Paragraph(replace_emojis(line[4:]), styles["CustomHeading2"]))

            elif re.match(r"\d+\.\s+\*\*(.*?)\*\*", line):
                flush_bullets()
                label = re.sub(r"\*\*", "", line)
                content.append(Paragraph(label, styles["CustomBody"]))

            elif re.match(r"- \*\*(.+?)\*\*: (.+)", line):
                flush_bullets()
                match = re.match(r"- \*\*(.+?)\*\*: (.+)", line)
                if match:
                    label, value = match.groups()
                    formatted = f"<b>{label}:</b> {value}"
                    content.append(Paragraph(formatted, styles["CustomBody"]))

            elif line.startswith("- "):
                bullet_buffer.append(line[2:])

            else:
                flush_bullets()
                content.append(Paragraph(line, styles["CustomBody"]))

        flush_bullets()
        doc.build(content)
        return file_path

    def generate_and_save_report(self) -> Dict[str, str]:
        prompt = self.generate_prompt()
        report_text = self.call_llm(prompt)
        self.final_report = report_text
        pdf_path = self.save_pdf(report_text)
        return report_text

def generate_final_report(
    origin_city: str,
    destination_city: str,
    num_days: int,
    flight_info: Dict[str, Any],
    weather_info: Dict[str, Any],
    attraction_info: List[Dict[str, Any]],
    restaurant_info: List[Dict[str, Any]],
    hotel_info: List[Dict[str, Any]],
    transport_info: Dict[str, Any],
    expense_report_text: str,
    outbound_date: str = "",
    return_date: str = "",
) -> Dict[str, str]:
    """
    Generate a final travel report and save it as a PDF.
    """
    report_generator = ReportGenerator(
        origin_city=origin_city,
        destination_city=destination_city,
        num_days=num_days,
        flight_info=flight_info,
        weather_info=weather_info,
        attraction_info=attraction_info,
        restaurant_info=restaurant_info,
        hotel_info=hotel_info,
        transport_info=transport_info,
        expense_report_text=expense_report_text,
        outbound_date=outbound_date,
        return_date=return_date,
        output_dir="generated_reports"  # Default output directory
    )
    
    return report_generator.generate_and_save_report()  
