"""Talks to Groq's free API. Tries a few models so the app keeps working
even if Groq retires one of them."""

import json
import os
import re

from dotenv import load_dotenv
from groq import (
    APIConnectionError, APIStatusError, AuthenticationError, Groq,
    RateLimitError,
)

load_dotenv()

# Tried in order for normal writing tasks. Set GROQ_MODEL in .env to put
# your own choice first.
FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
]

# Used for the JSON fact-check step specifically. gpt-oss-20b is a
# "reasoning" model — it spends part of its output budget thinking silently
# before writing the actual JSON, and on a full page of claims it can run
# out of room before finishing, which produces cut-off, invalid JSON. Plain
# instruction-following models are more reliable for structured output.
JSON_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]


class AIError(Exception):
    """A problem talking to the AI, with a message safe to show the user."""


def get_api_key():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        # On Hugging Face / Streamlit Cloud the key can live in "secrets".
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None
    if key and "your_groq_api_key" not in key:
        return key.strip()
    return None


_client = None


def _client_instance():
    global _client
    if _client is None:
        key = get_api_key()
        if not key:
            raise AIError("No Groq API key found. Add it to your .env file.")
        _client = Groq(api_key=key, max_retries=3, timeout=60)
    return _client


def _models(pool):
    chosen = [os.getenv("GROQ_MODEL")] + pool
    return list(dict.fromkeys(m for m in chosen if m))


def ask(prompt, system=None, json_mode=False, temperature=0.2, max_tokens=1800, models=None):
    """Send a prompt and return the reply text.

    json_mode nudges the model to reply with JSON only, via the prompt itself
    rather than Groq's strict response_format mode — that mode occasionally
    fails hard ("json_validate_failed") on longer prompts across every model,
    which is worse than just parsing the reply ourselves (see parse_json).
    """
    client = _client_instance()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    if json_mode:
        prompt += "\n\nRespond with ONLY the JSON object. No markdown fences, no commentary before or after it."
    messages.append({"role": "user", "content": prompt})

    pool = models or (JSON_MODELS if json_mode else FALLBACK_MODELS)
    last_error = None
    for model in _models(pool):
        try:
            reply = client.chat.completions.create(
                model=model, messages=messages,
                temperature=temperature, max_tokens=max_tokens,
            )
            text = (reply.choices[0].message.content or "").strip()
            if json_mode and parse_json(text) is None:
                last_error = ValueError(f"{model} didn't return valid JSON")
                continue  # try the next model instead of failing outright
            return text
        except AuthenticationError as exc:
            raise AIError(
                "Groq rejected your API key. Copy a fresh key from "
                "console.groq.com/keys into your .env file."
            ) from exc
        except RateLimitError as exc:
            last_error = exc  # free-tier limit hit; try a smaller model
        except APIConnectionError as exc:
            raise AIError("Couldn't reach Groq. Check your internet connection.") from exc
        except APIStatusError as exc:
            last_error = exc  # model retired or busy; try the next one

    if isinstance(last_error, RateLimitError):
        raise AIError("You've hit Groq's free usage limit for the moment. "
                      "Wait about a minute and try again.")
    raise AIError(f"Groq couldn't answer right now. Details: {last_error}")


def parse_json(text):
    """Read JSON from a reply, even if the model wrapped it in extra text
    or left a trailing comma (a common small-model slip)."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    candidates = [text]
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        candidates.append(text[start:end + 1])
    for candidate in candidates:
        for attempt in (candidate, re.sub(r",\s*([}\]])", r"\1", candidate)):
            try:
                return json.loads(attempt)
            except json.JSONDecodeError:
                continue
    return None
