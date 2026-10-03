import os
from google import genai
from dotenv import load_dotenv

class ProductionGenAIAssistant:
    """ Core GenAi Engine implementing an O(1) Bounded Memory buffer. 
      Optimizes payload size,reduces API token costs, and controls execution latency."""
    def __init__(self, model_name= "gemini-3.6-flash", max_history_turns: int = 2):
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv("GEMINI_API_KEY") # Resolve Gemini API Key
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable missing!")
        # Initialize Google GenAI Client   
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.max_history_turns = max_history_turns
        
        # Explicit Controlled History Array
        self.history_buffer = []
        print(f"Assistant Ready | Sliding History Window: Last {self.max_history_turns} messages")

    def send_prompt(self, user_message: str) -> str:
        # 1. Appends user prompt to buffer
        self.history_buffer.append({"role": "user", "parts": [{"text": user_message}]})
        
        # 2. Apply O(1) Tail-Slicing to bound memory and context token payload.
        if len(self.history_buffer) > self.max_history_turns:
            self.history_buffer = self.history_buffer[-self.max_history_turns:]
            print(f"\n[SYSTEM SLICE] Old turns dropped! Active buffer size: {len(self.history_buffer)}")

        # 3. Instantiate chat session with bounded history window.
        chat = self.client.chats.create(
            model=self.model_name,
            history=self.history_buffer
        )
        
        # 4. Dispatch payload to API with constrained history.
        response = chat.send_message(user_message)
        
        # 5. Sunc AI response back into local history buffer.
        self.history_buffer.append({"role": "model", "parts": [{"text": response.text}]})
        
        return response.text

    def print_history_debug(self):
        """Prints current active memory buffer state for latency and context inspection."""
        print("\n--- [DEBUG] Memory History Buffer ---")
        for idx, msg in enumerate(self.history_buffer):
            role = msg["role"].upper()
            text = msg["parts"][0]["text"][:50] # Display first 50 characters..
            print(f"{idx+1}. [{role}]: {text}...")
        print(f"Total Active Messages in Buffer: {len(self.history_buffer)}")
        print("------------------------------------\n")


if __name__ == "__main__":
    # Test Setup: Window = 2 (Maintains only the latest context window)
    assistant = ProductionGenAIAssistant(max_history_turns=2)

    print("\n--- Turn 1 ---")
    assistant.send_prompt("Mera naam Rahul hai aur main DU se CS padh raha hoon.")
    assistant.print_history_debug()

    print("\n--- Turn 2 ---")
    assistant.send_prompt("Mujhe Python pasand hai.")
    assistant.print_history_debug()

    print("\n--- Turn 3 (Truncation Test) ---")
    res = assistant.send_prompt("Mera naam kya hai?")
    print("AI Response 3:\n", res)
    assistant.print_history_debug()

