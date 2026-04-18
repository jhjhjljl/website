from datetime import date, datetime
from pathlib import Path

import frontmatter
import markdown as md
import yaml
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from config import templates


def _to_datetime(value) -> datetime:
	if isinstance(value, datetime):
		return value
	if isinstance(value, date):
		return datetime(value.year, value.month, value.day)
	return datetime.fromisoformat(str(value))


router = APIRouter(prefix="")

LOGS_DIR = Path(__file__).parent.parent / "content" / "logs"
IMGS_INDEX = Path(__file__).parent.parent / "content" / "imgs" / "index.yaml"


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
	return templates.TemplateResponse(request=request, name="index.html")


@router.get("/logs", response_class=HTMLResponse)
async def logs(request: Request):
	entries = []
	for path in LOGS_DIR.glob("*.md"):
		post = frontmatter.load(path)
		dt = _to_datetime(post["date"])
		entries.append({
			"slug": path.stem,
			"title": post["title"],
			"date": dt.strftime("%Y-%m-%d"),
			"datetime": dt.isoformat(),
			"_sort": dt,
		})
	entries.sort(key=lambda e: e["_sort"], reverse=True)
	return templates.TemplateResponse(request=request, name="logs.html", context={"entries": entries})


@router.get("/logs/{slug}", response_class=HTMLResponse)
async def log(request: Request, slug: str):
	path = LOGS_DIR / f"{slug}.md"
	if not path.exists():
		raise HTTPException(status_code=404)
	post = frontmatter.load(path)
	dt = _to_datetime(post["date"])
	return templates.TemplateResponse(request=request, name="log.html", context={
		"slug": slug,
		"title": post["title"],
		"date": dt.strftime("%Y-%m-%d"),
		"datetime": dt.isoformat(),
		"content": md.markdown(post.content),
	})


@router.get("/imgs", response_class=HTMLResponse)
async def imgs(request: Request):
	photos = yaml.safe_load(IMGS_INDEX.read_text())
	return templates.TemplateResponse(request=request, name="imgs.html", context={"photos": photos})


@router.get("/imgs/{slug}", response_class=HTMLResponse)
async def img(request: Request, slug: str):
	photos = yaml.safe_load(IMGS_INDEX.read_text())
	photo = next((p for p in photos if p["slug"] == slug), None)
	if not photo:
		raise HTTPException(status_code=404)
	return templates.TemplateResponse(request=request, name="img.html", context={"photo": photo})
