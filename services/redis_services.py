import redis.asyncio as redis
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_redis_client():
    # Create a global Redis client
    try:
        redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        yield redis_client
    except Exception as e:
        print(f"Error - {e}")
    finally:
        await redis_client.close()


# Set a value asynchronously
async def set_redis_value(key: str, text: str) -> None:
    old = await get_redis_values(key)
    old = old if old == "" else f"{old}\n"
    async with get_redis_client() as redis_client:
        await redis_client.set(key, f"{old}{text}", ex=3600)


# Get a redis value based on the key
async def get_redis_values(key: str) -> str:
    async with get_redis_client() as redis_client:
        value = await redis_client.get(key)
        return value if value else ""


# Flush the current Redis DB
async def flush_redis_db() -> None:
    async with get_redis_client() as redis_client:
        await redis_client.flushdb()
