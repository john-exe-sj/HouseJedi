# Import necessary classes from the uAgents library
from uagents import Agent, Context, Model
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Message(Model): 
    message: str
 
# Create an agent named alice
agent = Agent(
    name="Bob", 
    seed="backend_seed", 
    endpoint=["http://127.0.0.8001"], 
    port=8001, 
    mailbox=os.getenv("AGENT_KEY_BACKEND_MAILBOX")
)

FRONT_END_ADDR = "agent1q25keva9zp8hq3u6xr6jl8rkmadt0ddzvps3xttgkakjq0yt4ekpw05yan7"
 
# Function to be called when the agent is started
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    # Print a greeting message with the agent's name and its address
    print(f"Hello, I'm agent, my address is {ctx.agent.address}.")

@agent.on_interval(period=2)
async def send_message(ctx: Context): 
    await ctx.send(FRONT_END_ADDR, message=Message(message="HI FROM THE BACK"))
# Run the agent only when the script is executed directly
if __name__ == "__main__":
    agent.run()