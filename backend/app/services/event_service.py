import json
import logging
from app.core.redis_client import redis

logger = logging.getLogger("app.services.event")

class EventService:
    CHANNEL = "todo_updates"

    async def publish_todo_event(self, event_type: str, payload: dict) -> None:
        message = json.dumps({"type": event_type, "payload": payload})
        await redis.publish(EventService.CHANNEL, message)
        logger.debug("Published event %s", message)
