"""
Adapter: принимает list[str] headline‑ов, делает ОДИН запрос к ChatGPT
и возвращает list[dict] с полями score/topic/sentiment/summary.
"""

from __future__ import annotations
import json, time, random
from typing import Iterable, List, Dict, Any
import requests

from ai.config import TOKEN
from logger import Logger

ENDPOINT       = "https://api.proxyapi.ru/openai/v1/chat/completions"
MODEL          = "gpt-4o"
TEMPERATURE    = 0.2
MAX_TOKENS     = 2500          # хватает примерно на 1‑2 тыс. заголовков
RETRY_LIMIT    = 3
BACKOFF        = (1.5, 3.5)

SYSTEM_PROMPT = (
    "Ты — аналитик новостей.\n"
    "Получишь JSON‑массив строк (заголовков). "
    "Верни **точно такой же по длине** JSON‑массив, где каждый элемент:\n"
    "{"
    "\"topic\": str,               # ключевая тема в 1‑2 словах\n"
    "\"sentiment\": str,           # positive | neutral | negative\n"
    "}\n"
    "Ничего кроме JSON‑массива не пиши."
)

class ChatGPTRequestsAdapter:
    def __init__(self, *, api_key: str | None = None) -> None:
        self.api_key = api_key or TOKEN
        self.logger = Logger()

    # публичный метод
    def analyze(self, headlines: Iterable[str]) -> List[Dict[str, Any]]:
        headlines = list(headlines)
        raw = self._call_with_retry(headlines)
        try:
            parsed: List[Dict[str, Any]] = json.loads(raw)
            if len(parsed) != len(headlines):
                raise ValueError("size mismatch")
        except Exception as err:
            self.logger.log(f"[ChatGPTAdapter] JSON error: {err}")
            parsed = [{"error": "parse_fail"}] * len(headlines)

        return [{"headline": h, **a} for h, a in zip(headlines, parsed)]

    # ---------- retry‑обёртка ----------
    def _call_with_retry(self, headlines: List[str]) -> str:
        for attempt in range(1, RETRY_LIMIT + 1):
            try:
                return self._single_request(headlines)
            except (requests.HTTPError,
                    requests.ConnectionError) as exc:
                if attempt == RETRY_LIMIT:
                    self.logger.log(f"[ChatGPTAdapter] ERROR {exc}")
                    return "[]"
                pause = random.uniform(*BACKOFF)
                self.logger.log(
                    f"[ChatGPTAdapter] retry {attempt}/{RETRY_LIMIT} "
                    f"in {pause:.1f}s")
                time.sleep(pause)

    # единственный HTTP‑запрос
    def _single_request(self, headlines: List[str]) -> str:
        payload = {
            "model": MODEL,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",
                 "content": json.dumps(headlines, ensure_ascii=False)}
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        r = requests.post(ENDPOINT, headers=headers, json=payload)
        if r.status_code != 200:
            raise requests.HTTPError(f"{r.status_code}: {r.text}")
        return r.json()["choices"][0]["message"]["content"].strip().replace('json', '')
