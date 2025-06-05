#!/usr/bin/env python3
"""
Simple runner script for the Sequential Workflow example.

This script demonstrates the data processing pipeline with various input types.
"""

import sys
import os

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from data_processor import create_data_pipeline, demo_data_pipeline
from utils.session_helpers import ADKSessionManager, validate_config
from config import print_config_summary

def interactive_pipeline():
    """
    Run the data pipeline in interactive mode.
    """
    print("\n🔄 Interactive Data Pipeline")
    print("=" * 40)
    print("Enter text data to process through the pipeline:")
    print("- The pipeline will extract, validate, and format your data")
    print("- Type 'quit' or 'exit' to stop")
    print("-" * 40)
    
    # Create the pipeline and session
    try:
        pipeline = create_data_pipeline()
        session_manager = ADKSessionManager(app_name="interactive_pipeline")
        session_manager.create_runner(pipeline)
    except Exception as e:
        print(f"❌ Error setting up pipeline: {e}")
        return
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n📝 Enter data to process: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🔄 Processing through pipeline...")
            response = session_manager.run_query(f"Process this data: {user_input}")
            print(f"📊 Pipeline Result:\n{response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def run_examples():
    """
    Run predefined examples.
    """
    print("🚀 Running predefined pipeline examples...")
    demo_data_pipeline()

def main():
    """
    Main function to run the sequential workflow example.
    """
    print("🔄 Sequential Workflow - Data Processing Pipeline")
    print("=" * 60)
    
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
            interactive_pipeline()
        elif choice == "3":
            run_examples()
            interactive_pipeline()
        else:
            print("Invalid choice. Running examples by default.")
            run_examples()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 