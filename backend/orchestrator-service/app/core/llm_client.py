# app/core/llm_client.py
from typing import Dict, List, Optional, Union

from groq import Groq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from openai import OpenAI

from app.core.config import settings


class LLMClient:
    """
    Central LLM Client used by Orchestrator to call Groq / OpenAI providers.
    Fully compatible with LangGraph (ainvoke returns AIMessage)
    """

    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()

        if self.provider == "groq":
            self._init_groq()
        elif self.provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unsupported LLM provider '{settings.LLM_PROVIDER}'")

    def _init_groq(self):
        if not settings.GROQ_API_KEY:
            raise EnvironmentError("GROQ_API_KEY is missing.")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        # OpenAI-compatible endpoint powered by Groq (for Whisper, etc.)
        self.client_openai = OpenAI(
            api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1"
        )

    def _init_openai(self):
        if not settings.OPENAI_API_KEY:
            raise EnvironmentError("OPENAI_API_KEY is missing.")
        self.client = None
        self.client_openai = OpenAI(api_key=settings.OPENAI_API_KEY)

    # ——— Legacy sync method (still useful for simple calls) ———
    def chat_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1200,
    ) -> str:
        messages = self._build_messages(prompt, system_prompt)

        model = "llama-3.1-8b-instant"
        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()

    # ——— ASYNC: The one used by LangGraph & chains ———
    async def ainvoke(
        self,
        messages: List[Union[HumanMessage, SystemMessage]],
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1200,
    ) -> AIMessage:
        # print("\n[DEBUG][llm_client] Incoming LangChain messages:")
        # for m in messages:
        #     print(" - type:", m.type, "| content:", m.content)

        # Role conversion
        def convert_role(m):
            if isinstance(m, HumanMessage):
                return "user"
            if isinstance(m, AIMessage):
                return "assistant"
            if isinstance(m, SystemMessage):
                return "system"
            raise ValueError(f"Unknown message type: {m.type}")

        raw_messages = [
            {"role": convert_role(m), "content": m.content} for m in messages
        ]

        model = "llama-3.3-70b-versatile"
        response = self.client.chat.completions.create(
            model=model,
            messages=raw_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content.strip()
        return AIMessage(content=content)

    # ——— Special API for Whisper (audio STT) ———
    def transcribe_audio(self, file_bytes: bytes):
        """
        Uses Groq's Whisper-API-compatible transcription
        """
        return self.client_openai.audio.transcriptions.create(
            model="whisper-large-v3",
            file=("audio.wav", file_bytes, "audio/wav"),
            language="en",
        )

    # ——— Helper ———
    @staticmethod
    def _build_messages(
        prompt: str, system_prompt: Optional[str]
    ) -> List[Dict[str, str]]:
        msgs: List[Dict[str, str]] = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})
        return msgs


# Global instance used everywhere
llm = LLMClient()
