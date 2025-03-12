"""
LLM Model Provider Module

This module provides functionality to create and configure language model instances
from different providers using the LangChain library.
"""
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI

from writer.config import config
from writer.utils.logging_config import get_logger

# Get logger for this module
logger = get_logger(__name__)

class LLMProvider(Enum):
    """
    Enumeration of supported LLM providers.
    The string values match the expected values in the configuration.
    """
    OPENAI = "openai"     # OpenAI API (ChatGPT, GPT-4, etc.)
    DEEPSEEK = "deepseek" # DeepSeek AI platform


def get_llm_model(provider: LLMProvider, model_name):
    """
    Factory function to create and configure a language model instance based on the provider.
    
    Args:
        provider: The LLM provider to use (from LLMProvider enum)
        model_name: The name of the model to use with the selected provider
        
    Returns:
        A configured LangChain chat model instance
        
    Raises:
        ValueError: If an unknown provider is specified
    """
    logger.info(f"Creating LLM model instance for provider: {provider.value}, model: {model_name}")
    
    try:
        if provider == LLMProvider.OPENAI:
            # Create an OpenAI chat model instance
            logger.debug(f"Configuring OpenAI model with temperature={config.LLM_TEMPERATURE}, max_tokens={config.LLM_MAX_TOKENS}")
            model = ChatOpenAI(
                temperature=config.LLM_TEMPERATURE,
                api_key=config.OPENAI_API_KEY,
                model_name=model_name,
                max_tokens=config.LLM_MAX_TOKENS,
            )
            logger.info(f"Successfully created OpenAI model instance: {model_name}")
            return model
            
        elif provider == LLMProvider.DEEPSEEK:
            # Create a DeepSeek chat model instance using the OpenAI-compatible interface
            logger.debug(f"Configuring DeepSeek model with API base={config.DEEPSEEK_API_BASE}, max_tokens={config.LLM_MAX_TOKENS}")
            model = BaseChatOpenAI(
                model=model_name,
                openai_api_key=config.DEEPSEEK_API_KEY,
                openai_api_base=config.DEEPSEEK_API_BASE,
                max_tokens=config.LLM_MAX_TOKENS
            )
            logger.info(f"Successfully created DeepSeek model instance: {model_name}")
            return model
            
        else:
            logger.error(f"Unknown LLM provider: {provider}")
            raise ValueError(f'Unknown LLM type: {provider}')
            
    except Exception as e:
        logger.error(f"Error creating LLM model: {str(e)}", exc_info=True)
        raise
