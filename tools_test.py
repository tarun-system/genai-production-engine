"""Custom Tool Definitions and Assistant Class----------------------
---Defines mock functions (wather & math) and integrates them into the Gemini Assistant pipeline via Google GenAI SDK tool configurations."""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_current_weather(location: str) ->str:
    """Mock weather tool for state query simulation."""
    loc=location.lower()
    if "delhi" in loc:
        return "Delhi mein temperature 32ॱc hai aur aasmaan saaf hai."
    elif "mumbai" in loc:
        return "Mumbai mein temperature 28 c hai halaki baarish ho rahi hai."
    else:
        return f"{location} ka weather database mein available nahi hai."

def add_numbers(a: float,b:float) ->float:
        """Basic addition tool for mathematical operations."""
        return a+b
    
class GenaiAssistant:
    def __init__(self,model_name="gemini-3.6-flash",tools:list=None):
        load_dotenv()
        api_key=os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("NO API key found! Please check .env file.")
        self.client=genai.Client(api_key=api_key)
        self.model_name=model_name
        self.config=types.GenerateContentConfig(tools=tools if tools else [])

    def ask(self,prompt:str) ->str:
        chat=self.client.chats.create(model=self.model_name,config=self.config)
        response=chat.send_message(prompt)
        return response.text

    
if __name__=="__main__":
    ai_bot=GenaiAssistant(tools=[get_current_weather,add_numbers])
    print("--- Test 1: Normal Talk ---")
    print(ai_bot.ask("Hi,tum kaun ho? "))

    print("\n-------------------------------------------------------------------------")
    print("--- Test 2: Tool Call(weather) ---")
    print(ai_bot.ask("Delhi mein mausam kaisa hai? "))

    print("\n-------------------------------------------------------------------------")
    print("--- Test 3: Math Tool ---")
    print(ai_bot.ask("15.5 aru 24.5 ko add karke batao kitna hoga?"))
    
