from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import os
import time
import uuid


APP_SECRET = os.getenv("WEBHOOK_SHARED_SECRET", "")


class ToolCall(BaseModel):
    name: str = Field(..., description="Tool/function name")
    arguments: Dict[str, Any] = Field(default_factory=dict)


class TavusEvent(BaseModel):
    # Permissive model; we can tighten when schema is confirmed
    event_type: str = Field("tool_call")
    conversation_id: Optional[str] = None
    event_id: Optional[str] = None
    timestamp: Optional[float] = None
    tool: Optional[ToolCall] = None
    data: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "ignore"


app = FastAPI(title="Tavus Webhook Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_secret(req: Request) -> None:
    if not APP_SECRET:
        return  # disabled; dev mode
    provided = req.headers.get("x-webhook-secret") or req.headers.get("x-tavus-secret")
    if not provided or provided != APP_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")


handlers: Dict[str, Any] = {}


def register_tool(name: str):
    def _decorator(fn):
        handlers[name] = fn
        return fn
    return _decorator


@register_tool("summarize_discussion")
def handle_summarize(payload: TavusEvent) -> Dict[str, Any]:
    transcript = (
        (payload.tool.arguments.get("transcript") if payload.tool else None)
        or payload.data.get("transcript")
        or ""
    )
    # Placeholder: return a trivial summary
    bullets = [line.strip() for line in transcript.split("\n") if line.strip()][:5]
    return {"summary": bullets}


@register_tool("take_meeting_notes")
def handle_take_notes(payload: TavusEvent) -> Dict[str, Any]:
    content = (
        (payload.tool.arguments.get("content") if payload.tool else None)
        or payload.data.get("content")
        or ""
    )
    return {"notes": [content] if content else []}


@register_tool("cluster_ideas")
def handle_cluster(payload: TavusEvent) -> Dict[str, Any]:
    ideas = (
        (payload.tool.arguments.get("ideas") if payload.tool else None)
        or payload.data.get("ideas")
        or []
    )
    clusters = {}
    for idea in ideas:
        key = idea.split(" ")[0].lower() if idea else "misc"
        clusters.setdefault(key, []).append(idea)
    return {"clusters": clusters}


def process_event(evt: TavusEvent) -> None:
    # Idempotency example: a real impl would use a DB keyed by event_id
    tool_name = evt.tool.name if evt.tool else evt.data.get("tool")
    handler = handlers.get(tool_name)
    if not handler:
        # Unknown tool; just log
        print(f"[Webhook] Unknown tool: {tool_name}")
        return
    try:
        result = handler(evt)
        # TODO: If Tavus expects async result submission, call Tavus API here.
        print(f"[Webhook] Processed {tool_name} result=", result)
    except Exception as e:
        print(f"[Webhook] Handler error for {tool_name}: {e}")


@app.post("/tavus/callback")
async def tavus_callback(request: Request, background: BackgroundTasks):
    verify_secret(request)
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    evt = TavusEvent.model_validate({
        **payload,
        "event_id": payload.get("event_id") or str(uuid.uuid4()),
        "timestamp": payload.get("timestamp") or time.time(),
    })

    # Offload processing; ack quickly
    background.add_task(process_event, evt)
    return {"ok": True}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
