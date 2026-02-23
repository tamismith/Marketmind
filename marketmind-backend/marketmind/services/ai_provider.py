import os
from dataclasses import dataclass

import requests
from openai import OpenAI


@dataclass(frozen=True)
class TextGenerationRequest:
    system_prompt: str
    user_prompt: str
    model: str = "gpt-4o-mini"
    max_tokens: int = 180
    temperature: float = 0.7


@dataclass(frozen=True)
class ImageGenerationRequest:
    prompt: str
    width: int = 1024
    height: int = 1024
    cfg_scale: int = 7
    steps: int = 30
    samples: int = 1


class AIProviderError(Exception):
    pass


class AIProvider:
    def __init__(self) -> None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise AIProviderError("OPENAI_API_KEY is missing")

        self._openai_client = OpenAI(api_key=openai_api_key)
        self._stability_api_key = os.getenv("STABILITY_API_KEY")

    def generate_text(self, request: TextGenerationRequest) -> str:
        try:
            response = self._openai_client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": request.system_prompt},
                    {"role": "user", "content": request.user_prompt},
                ],
                max_tokens=request.max_tokens,
                temperature=request.temperature,
            )
            content = (response.choices[0].message.content or "").strip()
            if not content:
                raise AIProviderError("Empty text response from provider")
            return content
        except Exception as exc:
            raise AIProviderError(f"Text generation failed: {exc}") from exc

    def generate_image_base64(self, request: ImageGenerationRequest) -> str:
        if not self._stability_api_key:
            raise AIProviderError("STABILITY_API_KEY is missing")

        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                headers={
                    "Authorization": f"Bearer {self._stability_api_key}",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "text_prompts": [{"text": request.prompt}],
                    "cfg_scale": request.cfg_scale,
                    "steps": request.steps,
                    "samples": request.samples,
                    "height": request.height,
                    "width": request.width,
                },
                timeout=60,
            )
        except Exception as exc:
            raise AIProviderError(f"Image generation request failed: {exc}") from exc

        if response.status_code != 200:
            raise AIProviderError(
                f"Image generation failed: status={response.status_code}, body={response.text}"
            )

        artifacts = response.json().get("artifacts", [])
        if not artifacts:
            raise AIProviderError("Image generation returned no artifacts")

        image_base64 = artifacts[0].get("base64", "")
        if not image_base64:
            raise AIProviderError("Image generation returned empty image data")

        return image_base64
