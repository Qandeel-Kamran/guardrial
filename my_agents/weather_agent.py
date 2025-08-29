from agents import Agent, function_tool

@function_tool
def find_weather(city: str) -> str:
    return f"{city.title()} temperature is 35 degrees"

weather_agent = Agent(
    name="weatherAgent",
    instructions="""
    You are a helpful weather agent. 
    Whenever the user asks about the weather in a city, 
    use the `find_weather` tool with the correct city name to respond.
    Do not respond directly. Always use the tool.
    """,
    handoff_description="Handles weather-related queries for cities",
    tools=[find_weather],
)
