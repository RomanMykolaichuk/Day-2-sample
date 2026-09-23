import os
from pathlib import Path
from typing import Literal, Self

import groq
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from groq import AsyncGroq
from pydantic import BaseModel, Field, field_validator, model_validator

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = os.getenv("GROQ_MODEL", "").strip()

SYSTEM_INSTRUCTION = (
    "You are a helpful educational assistant. Explain clearly, be concise, "
    "and acknowledge uncertainty."
)
MAX_MESSAGES = 20
MAX_MESSAGE_CHARS = 4000
MAX_TOTAL_CHARS = 12000
MAX_OUTPUT_TOKENS = 512
REQUEST_TIMEOUT_SECONDS = 20.0

app = FastAPI(title="Day 3 Groq Chat API")


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_MESSAGE_CHARS)

    @field_validator("content")
    @classmethod
    def strip_and_reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message content cannot be blank.")
        return value


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=MAX_MESSAGES)

    @model_validator(mode="after")
    def validate_conversation(self) -> Self:
        if self.messages[-1].role != "user":
            raise ValueError("The last message must have role 'user'.")
        if sum(len(message.content) for message in self.messages) > MAX_TOTAL_CHARS:
            raise ValueError("Conversation is too large.")
        return self


class ChatResponse(BaseModel):
    reply: str
    model: str


@app.get("/api/health")
async def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "configured": bool(GROQ_API_KEY and GROQ_MODEL),
        "api_key_present": bool(GROQ_API_KEY),
        "model_present": bool(GROQ_MODEL),
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not GROQ_API_KEY or not GROQ_MODEL:
        raise HTTPException(
            status_code=503,
            detail="Groq is not configured. Set GROQ_API_KEY and GROQ_MODEL on the server.",
        )

    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        *[message.model_dump() for message in request.messages],
    ]

    try:
        async with AsyncGroq(
            api_key=GROQ_API_KEY,
            timeout=REQUEST_TIMEOUT_SECONDS,
            max_retries=0,
        ) as client:
            completion = await client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                max_completion_tokens=MAX_OUTPUT_TOKENS,
            )
    except groq.AuthenticationError:
        raise HTTPException(status_code=502, detail="Groq authentication failed.") from None
    except groq.PermissionDeniedError:
        raise HTTPException(
            status_code=502,
            detail="Groq denied access. Check API key permissions and model availability.",
        ) from None
    except groq.NotFoundError:
        raise HTTPException(
            status_code=502,
            detail="The configured Groq model is unavailable or was not found.",
        ) from None
    except groq.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Groq rate limit reached. Please try again later.",
        ) from None
    except groq.APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Groq did not respond before the server timeout.",
        ) from None
    except groq.APIConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Groq.",
        ) from None
    except groq.BadRequestError:
        raise HTTPException(
            status_code=502,
            detail="Groq rejected the request. Check that GROQ_MODEL is a currently available chat model.",
        ) from None
    except groq.APIStatusError:
        raise HTTPException(
            status_code=502,
            detail="Groq returned an upstream service error.",
        ) from None

    reply = completion.choices[0].message.content if completion.choices else None
    if not isinstance(reply, str) or not reply.strip():
        raise HTTPException(status_code=502, detail="Groq returned an empty response.")

    return ChatResponse(reply=reply.strip(), model=GROQ_MODEL)
