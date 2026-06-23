import asyncio
import json
import logging
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.redis_client import redis

router = APIRouter()
logger = logging.getLogger("app.api.v1.events")

@router.get("/stream", include_in_schema=False)
async def sse_stream(request: Request, current_user = Depends(get_current_user)):
    async def event_generator():
        pubsub = redis.pubsub()
        await pubsub.subscribe(EventService.CHANNEL)
        try:
            while True:
                if await request.is_disconnected():
                    break
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message["type"] == "message":
                    data = message["data"]
                    payload = json.loads(data)
                    # Ensure event belongs to the same user (optional, here we broadcast all)
                    yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0.1)
        finally:
            await pubsub.unsubscribe(EventService.CHANNEL)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
