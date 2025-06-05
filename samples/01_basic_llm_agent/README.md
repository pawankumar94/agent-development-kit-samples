# Basic LLM Agent Sample

This sample demonstrates how to create a simple LLM agent using Google's ADK. The agent can perform weather checks and mathematical calculations using custom tools.

## Features

- **Weather Tool**: Get weather information for any city
- **Calculator Tool**: Perform mathematical calculations
- **Natural Language Processing**: The agent decides which tool to use based on user input
- **Session Management**: Maintains conversation context

## Files

- `weather_assistant.py` - Main implementation of the weather assistant agent
- `run_example.py` - Simple script to run the agent with example queries
- `README.md` - This documentation

## How It Works

1. **Agent Creation**: Creates an LLMAgent with custom tools
2. **Tool Registration**: Registers weather and calculator functions as tools
3. **Query Processing**: Agent analyzes user input and selects appropriate tools
4. **Response Generation**: Returns natural language responses based on tool results

## Usage

### Basic Usage

```python
from weather_assistant import create_weather_agent
from utils.session_helpers import run_simple_query

# Create the agent
agent = create_weather_agent()

# Run a query
response = run_simple_query(agent, "What's the weather like in Tokyo?")
print(response)
```

### Advanced Usage

```python
from weather_assistant import create_weather_agent
from utils.session_helpers import ADKSessionManager

# Create session manager
session_manager = ADKSessionManager(app_name="weather_demo")

# Create agent and runner
agent = create_weather_agent()
runner = session_manager.create_runner(agent)

# Run multiple queries in the same session
queries = [
    "What's the weather in Paris?",
    "Calculate 15 * 8",
    "What about the weather in London?"
]

for query in queries:
    response = session_manager.run_query(query)
    print(f"Q: {query}")
    print(f"A: {response}\n")
```

## Running the Example

```bash
cd samples/01_basic_llm_agent
python run_example.py
```

## Key Concepts

### Tool Definition
Tools are Python functions with proper docstrings that the LLM can understand and use:

```python
def get_weather(city: str) -> dict:
    """Gets the current weather for a city.
    
    Args:
        city: The name of the city to get weather for.
        
    Returns:
        A dictionary with weather information
    """
    # Implementation here
```

### Agent Configuration
The LLMAgent is configured with:
- **Model**: The language model to use (e.g., gemini-2.0-flash)
- **Tools**: List of available tools
- **Instructions**: System prompt defining agent behavior
- **Description**: Brief description of agent purpose

### Session Management
Sessions maintain conversation context and allow for:
- Multi-turn conversations
- State persistence
- Error handling
- Event streaming

## Customization

You can easily customize this example by:

1. **Adding New Tools**: Create new functions and add them to the tools list
2. **Changing Instructions**: Modify the agent's system prompt
3. **Using Different Models**: Change the model parameter
4. **Adding Error Handling**: Implement custom error handling logic

## Next Steps

- Try the Sequential Workflow sample for ordered processing
- Explore the Parallel Processing sample for concurrent operations
- Check out the Multi-Agent System for complex orchestration 