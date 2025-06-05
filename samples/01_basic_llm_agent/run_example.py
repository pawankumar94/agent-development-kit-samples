#!/usr/bin/env python3
"""
Simple runner script for the Weather Assistant example.

This script provides an interactive way to test the weather assistant agent.
You can either run predefined examples or enter your own queries.
"""

import sys
import os

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from weather_assistant import create_weather_agent, demo_weather_assistant
from utils.session_helpers import ADKSessionManager, validate_config
from config import print_config_summary

def interactive_mode():
    """
    Run the weather assistant in interactive mode.
    """
    print("\n🤖 Interactive Weather Assistant")
    print("=" * 40)
    print("Type your questions or commands:")
    print("- Ask about weather: 'What's the weather in Paris?'")
    print("- Do calculations: 'Calculate 15 * 8'")
    print("- Get time: 'What time is it in Tokyo?'")
    print("- Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    # Create the agent and session
    try:
        agent = create_weather_agent()
        session_manager = ADKSessionManager(app_name="interactive_weather")
        session_manager.create_runner(agent)
    except Exception as e:
        print(f"❌ Error setting up agent: {e}")
        return
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤔 Thinking...")
            response = session_manager.run_query(user_input)
            print(f"🤖 Assistant: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def run_examples():
    """
    Run predefined examples.
    """
    print("🚀 Running predefined examples...")
    demo_weather_assistant()

def main():
    """
    Main function to run the weather assistant example.
    """
    print("🌤️  Weather Assistant - ADK Sample")
    print("=" * 50)
    
    # Check configuration
    if not validate_config():
        print("❌ Configuration error. Please check your setup.")
        print("Make sure you have set GOOGLE_API_KEY in your environment or .env file.")
        return
    
    # Print configuration summary
    print_config_summary()
    
    # Ask user what they want to do
    print("Choose an option:")
    print("1. Run predefined examples")
    print("2. Interactive mode")
    print("3. Both")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_examples()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            run_examples()
            interactive_mode()
        else:
            print("Invalid choice. Running examples by default.")
            run_examples()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 