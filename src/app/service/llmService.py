import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field       
from langchain_mistralai import ChatMistralAI
from app.dataModal.ExpenseDataModal import ExpenseDataModal

class LLMService:
    def __init__(self):
        load_dotenv()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (   
                    "system",
                    "You are an expert in extracting data from bank messages."
                    "You will be given a bank message and you have to extract only the relevant data(attributes) from the message."
                    "If you don't find value of any relevant attribute in the message, then return empty value for that attribute."
                    "The data should be in the form of json."
                ),
                (
                    "human", "{text}"
                )
            ]
        )
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.model_name = os.getenv("MODEL_NAME")
        self.llm = ChatMistralAI(api_key=self.api_key, model_name=self.model_name)
        self.runnable = self.prompt | self.llm.with_structured_output(schema=ExpenseDataModal)

    def runLLM(self, message):
        return self.runnable.invoke({"text": message})