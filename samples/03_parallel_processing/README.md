# Parallel Processing Sample

This sample demonstrates how to use ADK's ParallelAgent to execute multiple tasks concurrently. The example shows how to gather data from multiple sources simultaneously, significantly improving performance compared to sequential processing.

## Features

- **Concurrent Execution**: Multiple agents run simultaneously
- **Performance Optimization**: Faster processing through parallelization
- **Multi-Source Data**: Gather information from different sources
- **Result Aggregation**: Combine results from all parallel operations

## Files

- `data_aggregator.py` - Main implementation of the parallel data aggregation system
- `run_example.py` - Script to run the parallel processing with example queries
- `README.md` - This documentation

## How It Works

1. **Weather Agent**: Fetches weather data for specified cities
2. **News Agent**: Retrieves news information for given topics
3. **Stock Agent**: Gets stock market data for specified symbols
4. **Parallel Execution**: All agents run concurrently to maximize efficiency

## Usage

### Basic Usage

```python
from data_aggregator import create_data_aggregator
from utils.session_helpers import run_simple_query

# Create the aggregator
aggregator = create_data_aggregator()

# Run parallel data gathering
response = run_simple_query(aggregator, "Get data for New York weather, tech news, and AAPL stock")
print(response)
```

### Advanced Usage

```python
from data_aggregator import create_data_aggregator
from utils.session_helpers import ADKSessionManager
import time

# Create session manager
session_manager = ADKSessionManager(app_name="parallel_demo")

# Create aggregator and runner
aggregator = create_data_aggregator()
runner = session_manager.create_runner(aggregator)

# Time the parallel execution
start_time = time.time()
response = session_manager.run_query("Gather data for London, business news, and GOOGL")
end_time = time.time()

print(f"Response: {response}")
print(f"Execution time: {end_time - start_time:.2f} seconds")
```

## Running the Example

```bash
cd samples/03_parallel_processing
python run_example.py
```

## Performance Benefits

Parallel processing provides significant performance improvements:

- **Sequential**: 3 API calls × 1.5s each = ~4.5 seconds
- **Parallel**: max(1.5s, 1.2s, 1.8s) = ~1.8 seconds
- **Improvement**: ~60% faster execution

## Key Concepts

### Parallel Agent Configuration
```python
aggregator = ParallelAgent(
    name="data_aggregator",
    sub_agents=[weather_agent, news_agent, stock_agent],
    description="Gathers data from multiple sources concurrently"
)
```

### Concurrent Execution
- All sub-agents start simultaneously
- Each agent processes its portion independently
- Results are collected and combined
- Total time = max(individual execution times)

### Error Handling
- Individual agent failures don't stop others
- Partial results are still returned
- Error information is included in the response

## Customization

You can customize this example by:

1. **Adding New Data Sources**: Create additional agents for different APIs
2. **Modifying Timeouts**: Adjust simulated delays for testing
3. **Changing Aggregation Logic**: Modify how results are combined
4. **Adding Retry Logic**: Implement retry mechanisms for failed requests

## Use Cases

Parallel processing is ideal for:
- **API Aggregation**: Combining data from multiple services
- **Real-time Dashboards**: Gathering live data from various sources
- **Batch Processing**: Processing multiple independent items
- **Microservice Orchestration**: Coordinating multiple service calls

## Performance Considerations

- **I/O Bound Tasks**: Best suited for network calls, file operations
- **Independent Operations**: Tasks that don't depend on each other
- **Resource Management**: Consider API rate limits and system resources
- **Error Isolation**: Ensure one failure doesn't affect others

## Next Steps

- Try the Iterative Refinement sample for loop-based processing
- Explore the Multi-Agent System for complex orchestration
- Check out the Basic LLM Agent for simple tool usage 