import json_repair
from pydantic import BaseModel
from the_retry import retry
from google import genai
from google.genai import types
from core import config

client = genai.Client(api_key=config.GEMINI_KEY)


@retry(attempts=2, backoff=60, exponential_backoff=True)
def model_parser(
    prompt: str, model: BaseModel, content: str
) -> BaseModel:  # "Extract the article detail info from the text"
    final_chunk = "".join(
        chunk.text
        for chunk in client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=[prompt, content],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=model,
            ),
        )
    )
    json_data = json_repair.loads(final_chunk)
    return model(**json_data)
