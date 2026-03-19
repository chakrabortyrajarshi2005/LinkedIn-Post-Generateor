from dotenv import load_dotenv
load_dotenv()

import os
import getpass
from langchain_groq import ChatGroq

if "GROQ_CLOUD_API_KEY" not in os.environ:
    os.environ["GROQ_CLOUD_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_CLOUD_API_KEY"), model="llama-3.3-70b-versatile"
)

if __name__ == "__main__":
    response = llm.invoke("How to cook mutton kosha?")
    print(response.content)
