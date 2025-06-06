from redis.asyncio import Redis

from app.config.settings import project_settings

redis_conn = Redis(
    host=project_settings.REDIS_HOST,
    port=project_settings.REDIS_PORT,
    decode_responses=True,
)
