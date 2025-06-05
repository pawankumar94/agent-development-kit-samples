"""
Parallel Processing Example - Data Aggregator

This example demonstrates how to use ParallelAgent to execute multiple tasks
concurrently. The system gathers data from multiple sources simultaneously:
1. Weather data from weather APIs
2. News information from news sources  
3. Stock market data from financial APIs

All agents run in parallel to maximize performance and efficiency.
"""

import sys
import os
from typing import Dict, Any, List
import time
import random
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import GOOGLE_API_KEY, DEFAULT_MODEL, validate_required_config
from utils.session_helpers import validate_config

import google.generativeai as genai
from google.adk.agents import LlmAgent, ParallelAgent

# Configure Google AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def fetch_weather_data(city: str) -> Dict[str, Any]:
    """
    Fetches weather data for a specified city.
    
    This simulates an API call with realistic delays and data.
    In production, you would integrate with a real weather API.
    
    Args:
        city: The city to get weather data for
        
    Returns:
        Dictionary with weather information and metadata
    """
    # Simulate API call delay (realistic network latency)
    delay = random.uniform(0.8, 2.0)
    time.sleep(delay)
    
    # Mock weather data
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Snowy", "Foggy"]
    temperature = random.randint(-5, 35)
    humidity = random.randint(30, 90)
    wind_speed = random.randint(0, 25)
    
    return {
        "status": "success",
        "source": "weather_api",
        "city": city,
        "data": {
            "temperature": f"{temperature}°C",
            "condition": random.choice(conditions),
            "humidity": f"{humidity}%",
            "wind_speed": f"{wind_speed} km/h",
            "visibility": f"{random.randint(5, 20)} km"
        },
        "metadata": {
            "fetch_time": datetime.now().isoformat(),
            "api_delay": f"{delay:.2f}s",
            "data_freshness": "real-time"
        }
    }

def fetch_news_data(topic: str) -> Dict[str, Any]:
    """
    Fetches news data for a specified topic.
    
    This simulates a news API call with realistic content.
    In production, you would integrate with a real news API.
    
    Args:
        topic: The topic to get news for
        
    Returns:
        Dictionary with news information and metadata
    """
    # Simulate API call delay
    delay = random.uniform(1.0, 2.5)
    time.sleep(delay)
    
    # Mock news data
    headlines = [
        f"Breaking: Major developments in {topic} sector",
        f"Analysis: The future of {topic} looks promising",
        f"Expert opinion: {topic} trends to watch",
        f"Market update: {topic} stocks show strong performance",
        f"Innovation: New {topic} breakthrough announced"
    ]
    
    selected_headlines = random.sample(headlines, 3)
    article_count = random.randint(50, 500)
    
    return {
        "status": "success",
        "source": "news_api",
        "topic": topic,
        "data": {
            "headlines": selected_headlines,
            "total_articles": article_count,
            "trending_score": random.randint(60, 100),
            "sentiment": random.choice(["positive", "neutral", "mixed"])
        },
        "metadata": {
            "fetch_time": datetime.now().isoformat(),
            "api_delay": f"{delay:.2f}s",
            "sources_count": random.randint(10, 50)
        }
    }

def fetch_stock_data(symbol: str) -> Dict[str, Any]:
    """
    Fetches stock market data for a specified symbol.
    
    This simulates a financial API call with realistic market data.
    In production, you would integrate with a real financial API.
    
    Args:
        symbol: The stock symbol to get data for
        
    Returns:
        Dictionary with stock information and metadata
    """
    # Simulate API call delay
    delay = random.uniform(0.5, 1.8)
    time.sleep(delay)
    
    # Mock stock data
    base_price = random.uniform(50, 500)
    change = random.uniform(-20, 20)
    change_percent = (change / base_price) * 100
    volume = random.randint(100000, 10000000)
    
    return {
        "status": "success",
        "source": "financial_api",
        "symbol": symbol.upper(),
        "data": {
            "current_price": f"${base_price:.2f}",
            "change": f"{change:+.2f}",
            "change_percent": f"{change_percent:+.2f}%",
            "volume": f"{volume:,}",
            "market_cap": f"${random.randint(1, 100)}B",
            "pe_ratio": f"{random.uniform(10, 30):.1f}"
        },
        "metadata": {
            "fetch_time": datetime.now().isoformat(),
            "api_delay": f"{delay:.2f}s",
            "market_status": "open" if random.choice([True, False]) else "closed"
        }
    }

def create_data_aggregator() -> ParallelAgent:
    """
    Creates and configures the parallel data aggregation system.
    
    Returns:
        Configured ParallelAgent instance ready for use.
    """
    # Validate configuration
    if not validate_config():
        raise ValueError("Invalid configuration. Please check your API key.")
    
    # Create individual agents for each data source
    weather_agent = LlmAgent(
        name="weather_agent",
        model=DEFAULT_MODEL,
        tools=[fetch_weather_data],
        output_key="weather_info",
        instruction="""You are a weather data agent. When given a city name,
        call fetch_weather_data(city) and return the weather information.
        Extract the city name from the user's request and use it for the API call.""",
        description="Fetches weather information for specified cities"
    )
    
    news_agent = LlmAgent(
        name="news_agent",
        model=DEFAULT_MODEL,
        tools=[fetch_news_data],
        output_key="news_info",
        instruction="""You are a news data agent. When given a topic,
        call fetch_news_data(topic) and return the news information.
        Extract the topic from the user's request and use it for the API call.""",
        description="Fetches news information for specified topics"
    )
    
    stock_agent = LlmAgent(
        name="stock_agent",
        model=DEFAULT_MODEL,
        tools=[fetch_stock_data],
        output_key="stock_info",
        instruction="""You are a stock data agent. When given a stock symbol,
        call fetch_stock_data(symbol) and return the stock information.
        Extract the stock symbol from the user's request and use it for the API call.""",
        description="Fetches stock market information for specified symbols"
    )
    
    # Create the parallel aggregator
    aggregator = ParallelAgent(
        name="data_aggregator",
        sub_agents=[weather_agent, news_agent, stock_agent],
        description="Gathers weather, news, and stock data concurrently from multiple sources"
    )
    
    return aggregator

def demo_parallel_processing():
    """
    Demonstrates the parallel data aggregation with performance timing.
    """
    from utils.session_helpers import ADKSessionManager, print_session_info
    
    print("⚡ Parallel Data Aggregation Demo")
    print("=" * 50)
    
    # Create the aggregator
    try:
        aggregator = create_data_aggregator()
        print("✅ Parallel data aggregator created successfully!")
    except Exception as e:
        print(f"❌ Error creating aggregator: {e}")
        return
    
    # Create session manager
    session_manager = ADKSessionManager(app_name="parallel_aggregator_demo")
    runner = session_manager.create_runner(aggregator)
    
    # Print session info
    print_session_info(session_manager)
    
    # Example queries for parallel processing
    example_queries = [
        "Get data for Tokyo weather, technology news, and AAPL stock",
        "Fetch information for London weather, business news, and GOOGL stock",
        "Gather data for New York weather, sports news, and MSFT stock",
        "Collect info for Paris weather, health news, and TSLA stock"
    ]
    
    print("Running parallel data aggregation examples:")
    print("-" * 50)
    
    total_start_time = time.time()
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n{i}. Query: {query}")
        
        # Time individual query
        start_time = time.time()
        
        try:
            response = session_manager.run_query(query)
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"   ⏱️  Execution time: {execution_time:.2f} seconds")
            print(f"   📊 Response preview: {response[:150]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    
    print(f"\n" + "=" * 50)
    print(f"🏁 Demo completed!")
    print(f"📈 Total execution time: {total_time:.2f} seconds")
    print(f"⚡ Average per query: {total_time/len(example_queries):.2f} seconds")
    print("\n💡 Performance Note:")
    print("   - Each query runs 3 agents in parallel")
    print("   - Sequential execution would take ~3x longer")
    print("   - Parallel processing provides significant speedup!")

def benchmark_parallel_vs_sequential():
    """
    Demonstrates the performance difference between parallel and sequential execution.
    """
    print("\n🏃‍♂️ Performance Benchmark: Parallel vs Sequential")
    print("=" * 60)
    
    # This is a conceptual demonstration since we can't easily create
    # a sequential version with the same ADK structure
    print("📊 Theoretical Performance Comparison:")
    print("-" * 40)
    
    # Simulate timing data based on our mock delays
    sequential_time = 1.5 * 3  # Average delay × number of agents
    parallel_time = 1.5  # Max delay (since they run concurrently)
    improvement = ((sequential_time - parallel_time) / sequential_time) * 100
    
    print(f"Sequential execution: ~{sequential_time:.1f} seconds")
    print(f"Parallel execution:   ~{parallel_time:.1f} seconds")
    print(f"Performance improvement: {improvement:.1f}%")
    print(f"Speedup factor: {sequential_time/parallel_time:.1f}x")
    
    print("\n🎯 Key Benefits of Parallel Processing:")
    print("   ✅ Faster overall execution time")
    print("   ✅ Better resource utilization")
    print("   ✅ Improved user experience")
    print("   ✅ Scalable architecture")

if __name__ == "__main__":
    demo_parallel_processing()
    benchmark_parallel_vs_sequential() 