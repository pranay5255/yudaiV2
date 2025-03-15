import os
import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import logging

from app.base_eda import DataProfiler
from app.context_manager import ContextManager
from app.prompt_template_orchestrator import generate_prompt_template
from app.summary_agent_prompt_template import (
    generate_chart_prompt_template,
    example_chart_config,
    parse_llm_response
)

# Configure logging for terminal output
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class MockLLM:
    """Simple LLM mock for demonstration"""
    def generate(self, prompt: str) -> str:
        """Mock response based on prompt content"""
        if "Orchestrator Agent" in prompt:
            return "I'd like to understand more about your sales trends across different product categories."
        return json.dumps(example_chart_config())

def run_data_profiler(sample_data_path: str, output_dir: str) -> str:
    """Run data profiling on sample data"""
    logger.info("\n=== Running Data Profiler ===")
    
    profiler = DataProfiler(upload_dir=output_dir)
    profile_path = profiler.process_file(sample_data_path)
    logger.info(f"Profile generated at: {profile_path}")
    return profile_path

def run_context_manager(profile_path: str, output_dir: str) -> ContextManager:
    """Initialize and run context manager with mock data"""
    logger.info("\n=== Setting up Context ===")
    
    context_manager = ContextManager(
        context_file_path=f"{output_dir}/context.json",
        markdown_path=f"{output_dir}/context.md"
    )
    
    # Load and process profile
    with open(profile_path, 'r') as f:
        profile_data = json.load(f)
    
    # Update context with profile
    context_manager.update_dataset_profile(profile_data)
    
    # Add mock entries for testing
    context_manager.add_mock_entries()
    
    logger.info("Context initialized with sample data profile and mock entries")
    return context_manager

def run_orchestrator(context_manager: ContextManager) -> str:
    """Run the orchestrator agent"""
    logger.info("\n=== Running Orchestrator Agent ===")
    
    profile = context_manager.get_dataset_profile()
    prompt = generate_prompt_template(profile, turn=1)
    
    llm = MockLLM()
    response = llm.generate(prompt)
    
    logger.info(f"Orchestrator Response: {response}")
    return response

def run_summary_agent(context_manager: ContextManager) -> dict:
    """Run the summary agent to generate chart config"""
    logger.info("\n=== Running Summary Agent ===")
    
    profile = context_manager.get_dataset_profile()
    # Convert dictionary context to Context object
    from app.context_manager import Context
    raw_context = context_manager.get_context()
    context = Context(
        session_info=raw_context["session_info"],
        dataset_profile=raw_context["dataset_profile"],
        user_inputs=raw_context["user_inputs"],
        analysis_history=raw_context["analysis_history"]
    )
    
    chart_prompt = generate_chart_prompt_template(profile, context)
    
    llm = MockLLM()
    response = llm.generate(chart_prompt)
    chart_config = parse_llm_response(response)
    
    logger.info("Generated chart configuration:")
    logger.info(json.dumps(chart_config, indent=2))
    return chart_config

def main():
    """Run the complete pipeline"""
    logger.info("Starting dashboard configuration pipeline...")
    
    # Setup output directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Define paths
    sample_data_path = os.path.join(os.getcwd(), "app/data/sample_data.csv")
    
    # Run pipeline
    profile_path = run_data_profiler(sample_data_path, output_dir)
    context_manager = run_context_manager(profile_path, output_dir)
    orchestrator_response = run_orchestrator(context_manager)
    chart_config = run_summary_agent(context_manager)
    
    # Save final configuration
    config_path = f"{output_dir}/dashboard_config.json"
    with open(config_path, 'w') as f:
        json.dump(chart_config, f, indent=2)
    
    logger.info(f"\nFinal configuration saved to: {config_path}")

if __name__ == "__main__":
    main()
