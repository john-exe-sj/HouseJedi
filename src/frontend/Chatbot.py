# Import necessary classes from the uAgents library
from uagents import Agent, Context, Model
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import json
import os
import time


# Load environment variables from .env file
load_dotenv()

llm = OllamaLLM(model=os.getenv('LLM_MODEL_NAME'))

class Message(Model):
    message: str
 
# Create an agent named alice
agent = Agent(
    name="alice", 
    seed="frontend_seed", 
    endpoint=["http://localhost:8000/submit"], 
    port=8000, 
    mailbox=os.getenv("AGENT_KEY_FRONTEND_MAILBOX")
)

BACK_END_ADDR = "agent1q2wpcnltmzkckcg07cyyv080zge2vczecyx64df7hlj7x2uryvmcsjaagx8"

# Function to be called when the agent is started
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    # Print a greeting message with the agent's name and its address
    print(f"Hello, I'm agent {ctx.agent.name} and my address is {agent.address}.")


class Request(Model):
    text: str

class Response(Model):
    timestamp: int
    text: str
    agent_address: str

@agent.on_rest_post("/rest/post", Request, Response)
async def handle_post(ctx: Context, req: Request) -> Response:
    ctx.logger.info("Received POST request")
    request_json = json.loads(req)
    ctx.logger.info(request_json)
    # TODO: Reformat this and have it come from the JurisdictionModel.py
    return Response(
        text=f"Received: {req.text}",
        agent_address=ctx.agent.address,
        timestamp=int(time.time()),
    )


#@agent.on_message(model=Message)
#async def handle_message(ctx:Context, sender:str, message: Message): 
#    ctx.logger.info(f"Recieved message: {message.message}, from {sender}")
 
# Run the agent only when the script is executed directly
if __name__ == "__main__":
    agent.run()