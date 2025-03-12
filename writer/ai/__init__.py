"""
AI Package

This package contains modules for working with language models and processing content.
It provides a unified interface for different LLM providers and content processing.
"""

# Import the LLM provider functionality
from writer.ai.llm_model_provider import get_llm_model, LLMProvider

# Import the content processing functionality
from writer.ai.llm_processor import infer
