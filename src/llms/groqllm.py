from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv


class GroqLLM:
    def __init__(self):
        load_dotenv()
    
    def get_llm(self):
        try:
            print(os.getenv("GROQ_API_KEY"))
            os.environ["GROQ_API_KEY"] = self.groq_api_key=os.getenv("GROQ_API_KEY")
            llm=ChatGroq(api_key=self.groq_api_key, model="meta-llama/llama-4-maverick-17b-128e-instruct")
            return llm
        except Exception as e:
            raise ValueError("Error occured with exception: {e}")