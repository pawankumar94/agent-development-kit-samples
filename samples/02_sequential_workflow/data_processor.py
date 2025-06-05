"""
Sequential Workflow Example - Data Processing Pipeline

This example demonstrates how to create a sequential workflow that processes
data through multiple ordered steps:
1. Data Extraction - Extract structured information from raw text
2. Data Validation - Validate the extracted data
3. Data Formatting - Format the data for final output

Each agent in the sequence receives output from the previous agent as input.
"""

import sys
import os
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from config import GOOGLE_API_KEY, DEFAULT_MODEL, validate_required_config
from utils.session_helpers import validate_config

import google.generativeai as genai
from google.adk.agents import LlmAgent, SequentialAgent

# Configure Google AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def extract_data(input_text: str) -> Dict[str, Any]:
    """
    Extracts structured data from raw input text.
    
    Args:
        input_text: The raw text to extract data from
        
    Returns:
        Dictionary with extracted data including entities, keywords, and metadata
    """
    import re
    
    # Simple extraction logic - in production, use NLP libraries
    words = input_text.split()
    word_count = len(words)
    char_count = len(input_text)
    
    # Extract potential entities (capitalized words)
    entities = [word.strip('.,!?') for word in words if word[0].isupper() and len(word) > 1]
    
    # Extract numbers
    numbers = re.findall(r'\d+(?:\.\d+)?', input_text)
    
    # Extract keywords (words longer than 4 characters)
    keywords = [word.lower().strip('.,!?') for word in words if len(word) > 4]
    
    # Determine content type
    content_type = "general"
    if any(word.lower() in input_text.lower() for word in ["sales", "revenue", "profit", "business"]):
        content_type = "business"
    elif any(word.lower() in input_text.lower() for word in ["customer", "feedback", "review", "satisfaction"]):
        content_type = "customer_feedback"
    elif any(word.lower() in input_text.lower() for word in ["product", "launch", "feature", "development"]):
        content_type = "product"
    
    return {
        "status": "success",
        "original_text": input_text,
        "word_count": word_count,
        "character_count": char_count,
        "entities": entities[:5],  # Limit to top 5
        "numbers": numbers,
        "keywords": keywords[:10],  # Limit to top 10
        "content_type": content_type,
        "extraction_timestamp": datetime.now().isoformat(),
        "extracted_data": {
            "text": input_text,
            "length": char_count,
            "type": content_type,
            "key_elements": entities + keywords[:3]
        }
    }

def validate_data(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates the extracted data against quality rules.
    
    Args:
        extracted_data: The data extracted from the previous step
        
    Returns:
        Dictionary with validation results and quality metrics
    """
    validation_results = {
        "status": "success",
        "is_valid": True,
        "validation_errors": [],
        "quality_score": 0,
        "validation_timestamp": datetime.now().isoformat()
    }
    
    # Extract the data to validate
    if "extracted_data" not in extracted_data:
        validation_results["status"] = "error"
        validation_results["validation_errors"].append("No extracted_data found")
        validation_results["is_valid"] = False
        return validation_results
    
    data = extracted_data["extracted_data"]
    
    # Validation rules
    quality_score = 0
    
    # Rule 1: Minimum length
    if data.get("length", 0) >= 10:
        quality_score += 25
    else:
        validation_results["validation_errors"].append("Text too short (minimum 10 characters)")
    
    # Rule 2: Has meaningful content
    if data.get("key_elements") and len(data["key_elements"]) > 0:
        quality_score += 25
    else:
        validation_results["validation_errors"].append("No key elements identified")
    
    # Rule 3: Content type identified
    if data.get("type") != "general":
        quality_score += 25
    else:
        validation_results["validation_errors"].append("Generic content type")
    
    # Rule 4: Reasonable word count
    word_count = extracted_data.get("word_count", 0)
    if 5 <= word_count <= 1000:
        quality_score += 25
    else:
        validation_results["validation_errors"].append(f"Word count out of range: {word_count}")
    
    validation_results["quality_score"] = quality_score
    validation_results["is_valid"] = quality_score >= 50  # Minimum 50% quality
    validation_results["validated_data"] = data
    validation_results["original_extraction"] = extracted_data
    
    return validation_results

def format_data(validation_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formats the validated data for final output.
    
    Args:
        validation_result: The validation results from the previous step
        
    Returns:
        Dictionary with formatted final output
    """
    if validation_result.get("status") != "success":
        return {
            "status": "error",
            "error": "Cannot format invalid data",
            "original_error": validation_result
        }
    
    validated_data = validation_result.get("validated_data", {})
    quality_score = validation_result.get("quality_score", 0)
    is_valid = validation_result.get("is_valid", False)
    
    # Create formatted output
    formatted_output = {
        "status": "success",
        "processing_complete": True,
        "final_result": {
            "content": {
                "original_text": validated_data.get("text", ""),
                "content_type": validated_data.get("type", "unknown"),
                "key_elements": validated_data.get("key_elements", []),
                "length": validated_data.get("length", 0)
            },
            "quality": {
                "score": quality_score,
                "is_valid": is_valid,
                "grade": "A" if quality_score >= 75 else "B" if quality_score >= 50 else "C"
            },
            "metadata": {
                "processed_at": datetime.now().isoformat(),
                "pipeline_version": "1.0",
                "processing_steps": ["extraction", "validation", "formatting"]
            }
        }
    }
    
    # Add summary
    if is_valid:
        summary = f"Successfully processed {validated_data.get('type', 'general')} content with {quality_score}% quality score."
    else:
        summary = f"Processed content with quality issues (score: {quality_score}%)."
    
    formatted_output["summary"] = summary
    formatted_output["validation_errors"] = validation_result.get("validation_errors", [])
    
    return formatted_output

def create_data_pipeline() -> SequentialAgent:
    """
    Creates and configures the data processing pipeline.
    
    Returns:
        Configured SequentialAgent instance ready for use.
    """
    # Validate configuration
    if not validate_config():
        raise ValueError("Invalid configuration. Please check your API key.")
    
    # Create individual agents for each step
    extractor_agent = LlmAgent(
        name="data_extractor",
        model=DEFAULT_MODEL,
        tools=[extract_data],
        output_key="extraction_result",
        instruction="""You are a data extraction agent. 
        When given user input, call extract_data(input_text) with the provided text.
        Return only the extraction result.""",
        description="Extracts structured data from raw text input"
    )
    
    validator_agent = LlmAgent(
        name="data_validator",
        model=DEFAULT_MODEL,
        tools=[validate_data],
        output_key="validation_result",
        instruction="""You are a data validation agent.
        Take the extraction result from the previous step and call validate_data(extracted_data).
        Return only the validation result.""",
        description="Validates extracted data against quality rules"
    )
    
    formatter_agent = LlmAgent(
        name="data_formatter",
        model=DEFAULT_MODEL,
        tools=[format_data],
        output_key="final_result",
        instruction="""You are a data formatting agent.
        Take the validation result from the previous step and call format_data(validation_result).
        Return only the formatted final result.""",
        description="Formats validated data for final output"
    )
    
    # Create the sequential pipeline
    pipeline = SequentialAgent(
        name="data_processing_pipeline",
        sub_agents=[extractor_agent, validator_agent, formatter_agent],
        description="Processes data through extraction, validation, and formatting steps"
    )
    
    return pipeline

def demo_data_pipeline():
    """
    Demonstrates the data processing pipeline with example data.
    """
    from utils.session_helpers import ADKSessionManager, print_session_info
    
    print("📊 Data Processing Pipeline Demo")
    print("=" * 50)
    
    # Create the pipeline
    try:
        pipeline = create_data_pipeline()
        print("✅ Data processing pipeline created successfully!")
    except Exception as e:
        print(f"❌ Error creating pipeline: {e}")
        return
    
    # Create session manager
    session_manager = ADKSessionManager(app_name="data_pipeline_demo")
    runner = session_manager.create_runner(pipeline)
    
    # Print session info
    print_session_info(session_manager)
    
    # Example data to process
    example_data = [
        "Customer feedback indicates high satisfaction with our new product launch.",
        "Sales revenue increased by 25% this quarter compared to last year.",
        "The development team successfully delivered the new feature on schedule.",
        "Short text",  # This should trigger validation errors
        "Our business strategy focuses on customer-centric product development and innovation."
    ]
    
    print("Processing example data through the pipeline:")
    print("-" * 50)
    
    for i, data in enumerate(example_data, 1):
        print(f"\n{i}. Input: {data}")
        print("   Processing through pipeline...")
        
        try:
            response = session_manager.run_query(f"Process this data: {data}")
            print(f"   Result: {response[:200]}...")  # Truncate for readability
        except Exception as e:
            print(f"   Error: {e}")
    
    print("\n" + "=" * 50)
    print("Pipeline demo completed!")

if __name__ == "__main__":
    demo_data_pipeline() 