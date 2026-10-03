# GenAI Production Engine

A production-grade Generative AI backend architecture designed with state management and tool execution.

## Key Features
- **O(1) Bounded Memory Buffer:** Keeps context overhead constant regardless of conversation length.
- **Modular Tool Execution:** Extensible custom tools (weather query simulation & mathematical calculations) integrated with Gemini API.

## File Structure
- `test_memory.py` - Core memory buffer logic and conversation state management.
- `tools_test.py` - Custom tool definitions and Gemini assistant pipeline integration.

## Tech Stack
- Python 3.10+
- Google Gemini SDK (`google-genai`)
- `python-dotenv
