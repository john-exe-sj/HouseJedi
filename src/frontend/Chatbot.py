# Import necessary classes from the uAgents library
from uagents import Agent, Context, Model
from langchain_ollama import OllamaLLM
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
llm = OllamaLLM(model=os.getenv('LLM_MODEL_NAME'))
class Message(Model):
    message: str
 
# Create an agent named alice
agent = Agent(
    name="alice", 
    seed="frontend_seed", 
    endpoint=["http://127.0.0.8000"], 
    port=8000, 
    mailbox=os.getenv("AGENT_KEY_FRONTEND_MAILBOX")
)

BACK_END_ADDR = "agent1q2wpcnltmzkckcg07cyyv080zge2vczecyx64df7hlj7x2uryvmcsjaagx8"

# Function to be called when the agent is started
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    # Print a greeting message with the agent's name and its address
    print(f"Hello, I'm agent {ctx.agent.name} and my address is {agent.address}.")

@agent.on_event("message")
async def handle_message(ctx:Context, sender:str, message: Message): 
    ctx.logger.info(f"Recieved message: {message.message}, from {sender}")
 
# Run the agent only when the script is executed directly
if __name__ == "__main__":
    agent.run()