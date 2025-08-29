
import asyncio
import json
from typing import Any
from agents import (
    Agent,
    OpenAIResponsesModel,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_export_api_key,
    RunConfig,
)

from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
import os

from pydantic import BaseModel

load_dotenv(find_dotenv(), override=True)

api_key1 = os.getenv("OPENAI_API_KEY")

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_PATH")
model_name = os.getenv("GEMINI_MODEL_NAME")

set_tracing_export_api_key(str(api_key1))

client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(model=str(model_name), openai_client=client)

INDIAN_CITIES = {"delhi", "mumbai", "bangalore", "hyderabad", "kolkata", "chennai"}
US_CITIES = {"new york", "los angeles", "chicago", "houston", "miami", "boston"}

def contains_indian_city(text: str) -> bool:
    return any(city in text.lower() for city in INDIAN_CITIES)

def contains_us_city(text: str) -> bool:
    return any(city in text.lower() for city in US_CITIES)

def run_input_guardrail(input_text: str):
    if contains_indian_city(input_text):
        raise ValueError("❌ Blocked: Queries about Indian cities are not allowed.")
    return input_text

def run_output_guardrail(output_text: str):
    if contains_us_city(output_text):
        raise ValueError("❌ Blocked: Output mentions U.S. cities, which is restricted.")
    return output_text

config = RunConfig(model=model,
                #    before_agent=run_input_guardrail,
                #    after_agent=run_output_guardrail,
                   )



