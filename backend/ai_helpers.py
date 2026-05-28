"""AI-powered helpers: image-to-question extraction & similar-question generation."""
import json
import base64
import logging
import re
from typing import Optional

from emergentintegrations.llm.chat import LlmChat, UserMessage, FileContent

logger = logging.getLogger(__name__)

EXTRACT_SYSTEM = """You are an expert at extracting WAEC mathematics questions from images.
You will receive an image of a printed math question. Extract the question and return ONLY a JSON object — no prose, no markdown fences — with this exact shape:

{
  "question": "the question text with LaTeX wrapped in $...$ for inline and $$...$$ for display math",
  "options": ["option A", "option B", "option C", "option D"],
  "answer": "the correct option exactly as it appears in options (or your best inference)",
  "subtopic_guess": "one of: linear-equations, quadratic-equations, simultaneous-equations, indices, logarithms, variation, sequences-series, inequalities, trig-ratios, trig-identities, sine-cosine-rules, elevation-depression, bearings, circle-theorems, polygons, area-volume, similarity-congruence, coordinate-geometry",
  "difficulty_guess": "easy|medium|hard",
  "solution_steps": ["step 1...", "step 2...", "step 3..."]
}

Use $ for inline math and convert any fractions/exponents/roots to LaTeX. If options aren't visible, infer plausible 4 options. Steps must show full WAEC examiner working."""

SIMILAR_SYSTEM = """You are an expert WAEC Further Mathematics question setter.

Generate N original questions that test the EXACT SAME topic, lesson, subtopic, skill and difficulty as the source question.

Rules:
- Do not switch to another topic.
- Do not switch to a related but different skill.
- If the source question is on Sets, every generated question must also be on Sets.
- If the source question is on set intersection, generate set intersection questions only.
- If the source question is on set union, complement, subsets, Venn cardinality, De Morgan's Laws or combinatorial sets, stay within that exact skill.
- If the source question is on Logic, every generated question must stay inside Logic.
- If the source question is on implication, truth tables, negation, connectives, converse/contrapositive, equivalence, argument validity or fallacies, stay within that exact skill.
- Never generate statistics questions such as mean, median, mode, range or probability unless the source question itself is statistics.
- Include 4 plausible options and full step-by-step solutions.

Return ONLY a JSON array (no prose, no markdown fences) with this shape:
[
  {
    "question": "...with LaTeX in $...$ delimiters",
    "options": ["A", "B", "C", "D"],
    "answer": "exact value from options",
    "solution_steps": ["step 1", "step 2", "..."],
    "skill": "short skill label"
  },
  ...
]
"""

def _strip_json(text: str) -> str:
    """Remove markdown fences if Gemini wraps output."""
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    return t.strip()

async def extract_question_from_image(api_key: str, image_b64: str, mime_type: str = "image/jpeg") -> dict:
    chat = (
        LlmChat(api_key=api_key, session_id="extract-question", system_message=EXTRACT_SYSTEM)
        .with_model("gemini", "gemini-3-flash-preview")
    )
    msg = UserMessage(
        text="Please extract the WAEC math question from this image and return the JSON only.",
        file_contents=[FileContent(content_type=mime_type, file_content_base64=image_b64)],
    )
    raw = await chat.send_message(msg)
    cleaned = _strip_json(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # try to extract first {...}
        m = re.search(r"\{[\s\S]*\}", cleaned)
        if not m:
            raise ValueError(f"Could not parse JSON from model: {raw[:200]}") from e
        data = json.loads(m.group(0))
    return data

async def generate_similar_questions(api_key: str, source_question: dict, n: int = 3) -> list[dict]:
    prompt = f"""Generate {n} similar original practice questions.

MANDATORY CONTEXT:
- Topic ID: {source_question.get('topic', '?')}
- Topic name: {source_question.get('topic_name', '?')}
- Subtopic ID: {source_question.get('subtopic', '?')}
- Subtopic name: {source_question.get('subtopic_name','?')}
- Lesson title: {source_question.get('lesson_title', '?')}
- Required skill: {source_question.get('skill', 'same skill as source')}
- Difficulty: {source_question.get('difficulty','medium')}
- Diagnostic tags: {source_question.get('feedback_tags', [])}
- Remediation target: {source_question.get('recommendation', '')}

You must stay inside the exact lesson/subtopic and required skill above.

Question: {source_question['question']}
Options: {source_question.get('options', [])}
Correct answer: {source_question.get('answer', '?')}
Official solution steps: {source_question.get('solution_steps', [])}

Reject internally any question that is not in this exact topic/subtopic/skill before returning JSON."""

    chat = (
        LlmChat(api_key=api_key, session_id=f"similar-{source_question.get('id', 'x')}", system_message=SIMILAR_SYSTEM)
        .with_model("gemini", "gemini-3-flash-preview")
    )
    raw = await chat.send_message(UserMessage(text=prompt))
    cleaned = _strip_json(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r"\[[\s\S]*\]", cleaned)
        if not m:
            raise ValueError(f"Model output not valid JSON: {raw[:200]}")
        data = json.loads(m.group(0))
    if not isinstance(data, list):
        raise ValueError("Expected JSON array")
    return data
