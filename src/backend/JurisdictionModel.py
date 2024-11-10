# Import necessary classes from the uAgents library
from uagents import Agent, Context, Model
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_ollama import OllamaLLM
load_dotenv()
llm = OllamaLLM(model="llama3.2")
# Load all .docx files from a directory
directory_path = os.path.abspath("./src/backend/data")
loader = DirectoryLoader(directory_path, glob="*.docx", loader_cls=UnstructuredWordDocumentLoader)

# Load documents
documents = loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

# Initialize the embedding model

def get_emedding_model(): 
    embedding_model = OllamaEmbeddings(model="llama3.2")
    return embedding_model

db = Chroma.from_documents(
    documents=documents, 
    embedding=get_emedding_model(), 
    persist_directory=directory_path
)

 
agent = Agent(
    name="Bob", 
    seed="backend_seed", 
    endpoint=["http://localhost:8001/submit"], 
    port=8001, 
    mailbox=os.getenv("AGENT_KEY_BACKEND_MAILBOX")
)

FRONT_END_ADDR = "agent1q25keva9zp8hq3u6xr6jl8rkmadt0ddzvps3xttgkakjq0yt4ekpw05yan7"
 
# Function to be called when the agent is started
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    # Print a greeting message with the agent's name and its address
    print(f"Hello, I'm agent, my address is {ctx.agent.address}.")

class Message(Model): 
     jurisdictions: list[str]


@agent.on_message(model=Message)
async def handle_message(ctx:Context, sender:str, message: Message): 
    ctx.logger.info(f"Recieved message: {message.jurisdictions}")
    #TODO: Based on this list of jurisdictions, we compile documents from our filesystem or database. 
    # Parse through those files and return a list of codes with their descriptions or return the list of file-paths

    if message.jurisdictions:
        query = "Find codes given these list of jurisdictions: "

        for juridiction in message.jurisdictions:
            query += juridiction
        # Lo    ad environment variables from .env file
        docs = db.similarity_search(query)

        # Step 3: Prepare the prompt for the LLM
        prompt_data = ""
        ctx.logger.info("finished similarity search, compiling information.")
        for doc in docs:
            print(doc)
            prompt_data += f"{doc})\n"

        prompt = "Summarize what I need to know about constructing buildings in East Palo Alto"
        # Step 4: Create the final prompt
        final_prompt = f"Given the following information: {prompt_data}\n-----\n Answer this question: {prompt}"
        print(final_prompt)
        ctx.logger.info("Prompting llama3.2")
        # Step 5: Feed the prompt to the LLM
        response = await llm.ainvoke(final_prompt)
        if response: 
            print(response)

        
# Run the agent only when the script is executed directly
if __name__ == "__main__":
    agent.run()
