import time

from ..config import get_settings


class GeminiClient:
    """Small wrapper around the Google GenAI SDK.

    The app remains usable when Gemini is unavailable: callers can fall back
    to the deterministic local catalog engine.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = None
        self.types = None
        if self.settings.gemini_api_key:
            try:
                from google import genai
                from google.genai import types

                self.client = genai.Client(api_key=self.settings.gemini_api_key)
                self.types = types
            except ImportError:
                self.client = None

    @property
    def enabled(self) -> bool:
        return self.client is not None

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        text = str(exc).upper()
        return any(code in text for code in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500", "INTERNAL"))

    def generate(
        self,
        prompt: str,
        image_bytes: bytes | None = None,
        mime_type: str | None = None,
    ) -> str | None:
        if not self.client:
            return None

        contents: list = [prompt]
        if image_bytes:
            contents.append(
                self.types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type or "image/jpeg",
                )
            )

        last_error: Exception | None = None
        for attempt in range(4):
            try:
                response = self.client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=contents,
                    config=self.types.GenerateContentConfig(
                        max_output_tokens=5000,
                        response_mime_type="application/json",
                    ),
                )
                return getattr(response, "text", None)
            except Exception as exc:
                last_error = exc
                if not self._is_retryable(exc) or attempt == 3:
                    raise
                delay = 2 ** attempt
                print(f"Gemini temporary error; retrying in {delay}s...")
                time.sleep(delay)

        if last_error:
            raise last_error
        return None
