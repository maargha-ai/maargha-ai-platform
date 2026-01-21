from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from io import BytesIO


def cv_text_to_pdf(cv_text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    # ---------------- STYLES ----------------

    name_style = ParagraphStyle(
        "NameStyle",
        fontName="Helvetica-Bold",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    role_style = ParagraphStyle(
        "RoleStyle",
        fontName="Helvetica",
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    contact_style = ParagraphStyle(
        "ContactStyle",
        fontName="Helvetica",
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor("#1f4fd8"),
        spaceAfter=14,
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        fontName="Helvetica-Bold",
        fontSize=11,
        spaceBefore=14,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=4,
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=body_style,
        leftIndent=12,
    )

    elements = []

    # ---------------- PARSE INPUT ----------------

    lines = [l.strip() for l in cv_text.split("\n") if l.strip()]

    i = 0
    current_section = None

    while i < len(lines):
        line = lines[i]

        # ---------- NAME ----------
        if line.startswith("NAME:"):
            name = lines[i + 1]
            elements.append(Paragraph(name, name_style))
            i += 2
            continue

        # ---------- ROLE ----------
        if line.startswith("TARGET ROLE:"):
            role = line.replace("TARGET ROLE:", "").strip()
            elements.append(Paragraph(role, role_style))
            elements.append(Spacer(1, 4))
            i += 1
            continue

        # ---------- SECTION ----------
        if line.startswith("SECTION:"):
            current_section = line.replace("SECTION:", "").strip()

            elements.append(
                HRFlowable(
                    width="100%",
                    thickness=1,
                    color="black",
                    spaceBefore=8,
                    spaceAfter=8,
                )
            )
            elements.append(Paragraph(current_section.upper(), section_style))
            i += 1
            continue

        # ---------- SKILLS (two-column layout) ----------
        if current_section == "SKILLS" and ":" in line:
            skills_data = []
            while i < len(lines) and ":" in lines[i]:
                label, value = lines[i].split(":", 1)
                skills_data.append(
                    [
                        Paragraph(f"<b>{label.strip()}</b>", body_style),
                        Paragraph(value.strip(), body_style),
                    ]
                )
                i += 1

            table = Table(
                skills_data,
                colWidths=[140, 360],
                hAlign="LEFT",
            )
            table.setStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                ]
            )
            elements.append(table)
            continue

        # ---------- PROJECT TITLES ----------
        if current_section == "PROJECTS" and "|" in line:
            title, links = line.split("|", 1)

            table = Table(
                [
                    [
                        Paragraph(f"<b>{title.strip()}</b>", body_style),
                        Paragraph(
                            f'<font color="#1f4fd8">{links.strip()}</font>',
                            ParagraphStyle(
                                "LinkStyle",
                                parent=body_style,
                                alignment=TA_LEFT,
                            ),
                        ),
                    ]
                ],
                colWidths=[360, 140],
            )
            elements.append(table)
            i += 1
            continue

        # ---------- BULLETS ----------
        if line.startswith("-"):
            elements.append(
                Paragraph(f"• {line[1:].strip()}", bullet_style)
            )
            i += 1
            continue

        # ---------- NORMAL TEXT ----------
        elements.append(Paragraph(line, body_style))
        i += 1

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
