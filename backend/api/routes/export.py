"""
Export API routes
"""
import html
import io
import textwrap

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from database.models import Base, NovelProject

router = APIRouter(prefix="/export", tags=["export"])

MAX_LINE_CHARS = 100

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _get_project(project_id: str) -> NovelProject:
    db = SessionLocal()
    try:
        project = db.query(NovelProject).filter(NovelProject.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    finally:
        db.close()


@router.post("/projects/{project_id}/markdown")
def export_markdown(project_id: str):
    project = _get_project(project_id)
    md = f"# {project.title}\n\n"
    if project.description:
        md += f"{project.description}\n\n"
    if project.content:
        md += project.content
    filename = f"{project.title}.md".replace(" ", "_")
    return Response(
        content=md,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/projects/{project_id}/pdf")
def export_pdf(project_id: str):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError:
        raise HTTPException(status_code=501, detail="reportlab not available")

    project = _get_project(project_id)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    MAX_LINE_CHARS = 100
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, project.title)
    c.setFont("Helvetica", 12)
    y = height - 108
    content = project.content or ""
    for paragraph in content.split("\n"):
        for line in textwrap.wrap(paragraph, width=MAX_LINE_CHARS) or [""]:
            if y < 72:
                c.showPage()
                y = height - 72
                c.setFont("Helvetica", 12)
            c.drawString(72, y, line)
            y -= 16
    c.save()
    buf.seek(0)
    filename = f"{project.title}.pdf".replace(" ", "_")
    return Response(
        content=buf.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/projects/{project_id}/epub")
def export_epub(project_id: str):
    try:
        import ebooklib
        from ebooklib import epub
    except ImportError:
        raise HTTPException(status_code=501, detail="ebooklib not available")

    project = _get_project(project_id)
    book = epub.EpubBook()
    book.set_title(project.title)
    chapter = epub.EpubHtml(title=project.title, file_name="chapter.xhtml", lang="zh")
    chapter.content = f"<h1>{html.escape(project.title)}</h1><p>{html.escape(project.content or '')}</p>"
    book.add_item(chapter)
    book.spine = ["nav", chapter]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    buf = io.BytesIO()
    epub.write_epub(buf, book)
    buf.seek(0)
    filename = f"{project.title}.epub".replace(" ", "_")
    return Response(
        content=buf.read(),
        media_type="application/epub+zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
