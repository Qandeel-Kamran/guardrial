# def main():
#     print("Hello from guardrial!")


# if __name__ == "__main__":
#     main()



from typing import Literal
from agents import (
    Agent,
    HandoffInputData,
    RunContextWrapper,
    Runner,
    RunConfig,
    TResponseInputItem,
    handoff,
)
from pydantic import BaseModel

from my_agents.weather_agent import weather_agent
from my_agents.hotel_agent import hotel_agent
from my_agents.flight_agent import flight_agent
from my_config import model
from agents.extensions import handoff_filters

import asyncio



class Users(BaseModel):
    name: str
    role: Literal["admin", "basic", "super user"]
    age: int

async def handoff_permission(ctx: RunContextWrapper[Users], agents: Agent) -> bool:
    if ctx.context.age > 30:
        return True
    if ctx.context.role == "admin":
        return True
    return False

def handoff_filter(data: HandoffInputData) -> HandoffInputData:
    data = handoff_filters.remove_all_tools(data)
    history = data.input_history[-2:]
    return HandoffInputData(
        input_history=history,
        new_items=data.new_items,
        pre_handoff_items=data.pre_handoff_items,
    )

triage_agent = Agent(
    name="TriageAgent",
    instructions="""
    You are a triage agent. Hand off to flight, hotel or weather agent 
    if the user asks for it. Otherwise, respond yourself.
    """,
    handoffs=[
        handoff(
            agent=weather_agent,
            tool_name_override="handoff_weatheragent",
            tool_description_override="Hand off to weather agent to get the weather information.",
            is_enabled=handoff_permission,
            input_filter=handoff_filter,
        ),
        hotel_agent,
        flight_agent,
    ],
    handoff_description="""
    This triage agent hands off to flight, hotel, or weather agent 
    if the user asks. Otherwise, it responds itself.
    """,
)

# Append the triage agent to the handoff lists
weather_agent.handoffs.append(triage_agent)
flight_agent.handoffs.append(triage_agent)
hotel_agent.handoffs.append(triage_agent)

# ✅ UPDATED MAIN FUNCTION
async def main():
    user = Users(name="fatima", role="admin", age=15)
    start_agent = triage_agent

    while True:
        user_prompt = input("enter your query here: ")
        if user_prompt.lower() == "exit":
            break

        # Send only the current input, not the full history
        input_data: list[TResponseInputItem] = [
            {"role": "user", "content": user_prompt}
        ]

        result = await Runner.run(
            start_agent,
            input=input_data,
            run_config=RunConfig(model=model, tracing_disabled=False),
            context=user,
        )

        print(result.final_output)

        # Optional: update the start_agent if needed
        start_agent = result.last_agent

# Run the async main function
asyncio.run(main())
