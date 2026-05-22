"""WAEC Online (waeconline.org.ng) past paper scraper.

Fetches a paper's question pages, parses text + math-image URLs,
and uses Gemini Vision to convert each theory question into an MCQ
(4 options) suitable for our practice/exam flow.
"""
from __future__ import annotations

import asyncio
import base64
import logging
import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from emergentintegrations.llm.chat import LlmChat, UserMessage, FileContent

logger = logging.getLogger(__name__)

BASE = "https://waeconline.org.ng/e-learning/Further/"

# Catalog of available WAEC Further Mathematics papers (29 papers, 2008–2023).
WAEC_PAPERS = [
    {"label": "WASSCE School 2023",          "year": 2023, "url": BASE + "furth240jc.html"},
    {"label": "WASSCE School 2022",          "year": 2022, "url": BASE + "furth235mc.html"},
    {"label": "WASSCE Private 1st 2022",     "year": 2022, "url": BASE + "furth235jc.html"},
    {"label": "WASSCE Private 2nd 2022",     "year": 2022, "url": BASE + "furth235ac.html"},
    {"label": "WASSCE Private 2nd 2021",     "year": 2021, "url": BASE + "furth230ac.html"},
    {"label": "WASSCE Private 1st 2020",     "year": 2020, "url": BASE + "furth230ac.html"},
    {"label": "WASSCE School 2019",          "year": 2019, "url": BASE + "furth228mc.html"},
    {"label": "WASSCE Private 1st 2019",     "year": 2019, "url": BASE + "furth228jc.html"},
    {"label": "WASSCE Private 2nd 2019",     "year": 2019, "url": BASE + "furth2019cm.html"},
    {"label": "WASSCE School 2018",          "year": 2018, "url": BASE + "furth227mc.html"},
    {"label": "WASSCE Private 1st 2018",     "year": 2018, "url": BASE + "furth227jc.html"},
    {"label": "WASSCE Private 2nd 2018",     "year": 2018, "url": BASE + "furth227ac.html"},
    {"label": "WASSCE School 2017",          "year": 2017, "url": BASE + "furth226mc.html"},
    {"label": "WASSCE Private 2017",         "year": 2017, "url": BASE + "furth226nc.html"},
    {"label": "WASSCE School 2016",          "year": 2016, "url": BASE + "furth225mc.html"},
    {"label": "WASSCE Private 2016",         "year": 2016, "url": BASE + "furth225nc.html"},
    {"label": "WASSCE 2015 May/Jun",         "year": 2015, "url": BASE + "furth224mc.html"},
    {"label": "WASSCE 2014 Private",         "year": 2014, "url": BASE + "furth223nc.html"},
    {"label": "WASSCE 2014 May/Jun",         "year": 2014, "url": BASE + "furth223mc.html"},
    {"label": "WASSCE 2013 May/Jun",         "year": 2013, "url": BASE + "furth222mc.html"},
    {"label": "WASSCE 2013 Private",         "year": 2013, "url": BASE + "furth222nc.html"},
    {"label": "WASSCE 2012 Private",         "year": 2012, "url": BASE + "furth221nc.html"},
    {"label": "WASSCE 2011 Private",         "year": 2011, "url": BASE + "furth220nc.html"},
    {"label": "WASSCE 2011 May/Jun",         "year": 2011, "url": BASE + "furth220mc.html"},
    {"label": "WASSCE 2010 Private",         "year": 2010, "url": BASE + "furth219nc.html"},
    {"label": "WASSCE 2009 May/Jun",         "year": 2009, "url": BASE + "furth218mc.html"},
    {"label": "WASSCE 2009 Private",         "year": 2009, "url": BASE + "furth218nc.html"},
    {"label": "WASSCE 2008 May/Jun",         "year": 2008, "url": BASE + "furth217mc.html"},
    {"label": "WASSCE 2008 Private",         "year": 2008, "url": BASE + "furth217nc.html"},
]


async def _fetch(client: httpx.AsyncClient, url: str) -> str:
    r = await client.get(url, timeout=30.0, follow_redirects=True)
    r.raise_for_status()
    return r.text


async def _fetch_bytes(client: httpx.AsyncClient, url: str) -> bytes:
    r = await client.get(url, timeout=30.0, follow_redirects=True)
    r.raise_for_status()
    return r.content


def _parse_paper_index(html: str, paper_url: str) -> list[str]:
    """Return ordered list of question-page URLs (e.g. mathsXXXmq1.html)."""
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    seen = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        m = re.search(r"q(\d+)\.html$", href, re.I)
        if m:
            full = urljoin(paper_url, href)
            if full not in seen:
                seen.add(full)
                urls.append((int(m.group(1)), full))
    urls.sort(key=lambda x: x[0])
    return [u for _, u in urls]


def _parse_question_page(html: str, base_url: str) -> dict:
    """Extract text + image URLs from a question page.

    Returns: { question_text, observation_text, image_urls (list[str]) }
    """
    soup = BeautifulSoup(html, "html.parser")
    # remove nav and menu blocks
    for el in soup.find_all(["script", "style"]):
        el.decompose()

    page_text = soup.get_text(separator="\n", strip=True)

    # split on "Observation" if present
    question_text, observation_text = page_text, ""
    m = re.search(r"\bObservation\b", page_text, re.I)
    if m:
        question_text = page_text[: m.start()].strip()
        observation_text = page_text[m.end():].strip()

    # extract image URLs (math snippets)
    image_urls = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if "clip_image" in src or "image" in src.lower():
            image_urls.append(urljoin(base_url, src))

    # strip the boilerplate navigation header before the question
    question_text = re.sub(r"General Mathematics Paper \d+.*?\d{4}", "", question_text)
    question_text = re.sub(r"Subject Home.*?13", "", question_text, flags=re.S)
    question_text = re.sub(r"Menu.*?Strength", "", question_text, flags=re.S)
    question_text = question_text.strip()

    return {
        "question_text": question_text,
        "observation_text": observation_text,
        "image_urls": image_urls,
    }


EXTRACT_TO_MCQ_SYSTEM = """You convert real WAEC FURTHER MATHEMATICS (Elective) past questions into one of two structured shapes suitable for student practice.

You will receive:
- The original WAEC Further Maths theory question text (Paper 2)
- The chief examiner's observation/solution text
- Inline math expressions as attached images (read these carefully)

Decide between two shapes:

**A) Multiple-choice ("objective")** — preferred when the question has a single numeric/symbolic answer:
{
  "question_type": "objective",
  "question": "the question (LaTeX in $...$)",
  "options": ["A", "B", "C", "D"],
  "answer": "exact match to one option",
  "subtopic_guess": "...",
  "difficulty_guess": "easy|medium|hard",
  "solution_steps": ["Step 1 ...", "..."]
}

**B) Theory ("theory")** — when the question is multi-part / requires construction / produces a list of answers:
{
  "question_type": "theory",
  "question": "the question (preserve sub-parts (a), (b), (c) with LaTeX)",
  "answer": "concise final answer(s), e.g. 'a) k=3, b) area = 5'",
  "subtopic_guess": "...",
  "difficulty_guess": "easy|medium|hard",
  "solution_steps": ["Step 1 ...", "..."]
}

Rules:
- subtopic_guess must be one of (FURTHER MATHS subtopics): measures-of-location, measures-of-spread, correlation, probability, perms-combinations, limits, differentiation, applications-differentiation, integration, applications-integration, vector-algebra-2d, vectors-3d, magnitude-direction, scalar-product, vectors-applications.
- For objective: 3 plausible distractors based on common student errors. The answer field must EXACTLY match one option string.
- solution_steps: mirror the examiner's working in clear, numbered prose (5-10 short steps).
- Output a single JSON object only — no commentary, no markdown fences."""


def _strip_json(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()


def _fix_latex_in_json(s: str) -> str:
    """Gemini sometimes outputs unescaped backslashes for LaTeX commands inside JSON strings
    (e.g. "\sin" instead of "\\sin"). Escape any `\X` where X is not a valid JSON escape char."""
    # Valid JSON escapes: \" \\ \/ \b \f \n \r \t \uXXXX
    return re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', s)


def _safe_json_loads(raw: str) -> dict | list | None:
    import json as _json
    cleaned = _strip_json(raw)
    for attempt in (cleaned, _fix_latex_in_json(cleaned)):
        try:
            return _json.loads(attempt)
        except _json.JSONDecodeError:
            continue
    # last attempt: extract first {...} or [...] and try again
    for pat in (r"\{[\s\S]*\}", r"\[[\s\S]*\]"):
        m = re.search(pat, cleaned)
        if m:
            for variant in (m.group(0), _fix_latex_in_json(m.group(0))):
                try:
                    return _json.loads(variant)
                except _json.JSONDecodeError:
                    continue
    return None


async def _gemini_to_mcq(api_key: str, q: dict, year: int, attempt: int = 0) -> dict | None:
    """Use Gemini Vision to convert a scraped question to MCQ JSON.

    Returns None on unrecoverable failure.
    """
    import json as _json
    try:
        async with httpx.AsyncClient() as client:
            file_contents = []
            for url in q["image_urls"][:12]:  # cap to keep payload sane
                try:
                    blob = await _fetch_bytes(client, url)
                    if not blob:
                        continue
                    mime = "image/png" if url.lower().endswith(".png") else "image/jpeg"
                    file_contents.append(FileContent(
                        content_type=mime,
                        file_content_base64=base64.b64encode(blob).decode(),
                    ))
                except Exception:
                    continue

        prompt = f"WAEC year: {year}\n\nQuestion text:\n{q['question_text'][:3000]}\n\nExaminer observation:\n{q['observation_text'][:3000]}"
        chat = LlmChat(
            api_key=api_key,
            session_id=f"waec-import-{year}-{attempt}",
            system_message=EXTRACT_TO_MCQ_SYSTEM,
        ).with_model("gemini", "gemini-3-flash-preview")
        msg = UserMessage(text=prompt, file_contents=file_contents or None)
        raw = await chat.send_message(msg)
        data = _safe_json_loads(raw)
        if data is None:
            logger.warning("Gemini returned non-JSON: %s", raw[:200])
        return data
    except Exception as e:
        logger.exception("Gemini extract failed: %s", e)
        return None


async def extract_paper(api_key: str, paper_url: str, year: int, max_questions: int = 13) -> dict:
    """Scrape a paper and convert each question to MCQ JSON.

    Returns {paper_url, year, questions: [...]}
    """
    async with httpx.AsyncClient(headers={"User-Agent": "WAEC-Math-AI/1.0"}) as client:
        index_html = await _fetch(client, paper_url)
        q_urls = _parse_paper_index(index_html, paper_url)
        if not q_urls:
            return {"paper_url": paper_url, "year": year, "questions": [], "error": "No question links found"}
        q_urls = q_urls[:max_questions]

        # scrape question pages concurrently (bounded)
        async def scrape_one(url: str) -> dict:
            html = await _fetch(client, url)
            data = _parse_question_page(html, url)
            data["source_url"] = url
            return data

        sem = asyncio.Semaphore(4)
        async def with_sem(url):
            async with sem:
                try:
                    return await scrape_one(url)
                except Exception as e:
                    logger.warning("scrape failed %s: %s", url, e)
                    return None
        scraped = await asyncio.gather(*[with_sem(u) for u in q_urls])
        scraped = [s for s in scraped if s]

    # Convert each to MCQ via Gemini (concurrent, capped)
    sem2 = asyncio.Semaphore(3)
    async def convert_one(q: dict, idx: int):
        async with sem2:
            mcq = await _gemini_to_mcq(api_key, q, year, attempt=idx)
            if not mcq:
                return None
            mcq["source_url"] = q.get("source_url")
            mcq["original_text"] = q["question_text"][:500]
            return mcq

    converted = await asyncio.gather(*[convert_one(q, i) for i, q in enumerate(scraped)])
    converted = [c for c in converted if c]
    return {"paper_url": paper_url, "year": year, "questions": converted, "total_scraped": len(scraped)}
