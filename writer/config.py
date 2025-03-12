"""
Configuration settings for the AI Content Writer application.
Uses pydantic_settings to load configuration from environment variables and .env file.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings class that defines all configuration parameters.
    Default values are provided where appropriate.
    """
    # General LLM settings
    LLM_PROVIDER: str = "openai"  # The LLM provider to use (openai or deepseek)
    LLM_MODEL: str = "gpt-4o"     # The model name to use with the selected provider
    LLM_TEMPERATURE: float = 0.0  # Controls randomness in responses (0.0 to 1.0)
    LLM_MAX_TOKENS: int = 1024    # Maximum number of tokens in the response
    
    # OPENAI specific settings
    OPENAI_API_KEY: str           # API key for OpenAI services

    # DEEPSEEK specific settings
    DEEPSEEK_API_KEY: str         # API key for DeepSeek services
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com"  # Base URL for DeepSeek API

    # Tavily search engine settings
    TAVILY_API_KEY: str           # API key for Tavily search services
    TAVILY_API_URL: str = "https://api.tavily.ai"  # Base URL for Tavily API
    TAVILY_SEARCH_DEPTH: str = "basic"  # Search depth (basic or advanced)
    TAVILY_INCLUDE_ANSWER: bool = True  # Include AI-generated answer in results
    TAVILY_TOPIC: str = "news"    # Default search topic
    TAVILY_INCLUDE_RAW_CONTENT: bool = True  # Include raw content in search results
    TAVILY_MAX_RESULTS: int = 3   # Maximum number of search results to return

    class Config:
        """Configuration for the Settings class"""
        env_file = ".env"         # Load settings from .env file
        env_file_encoding = "utf-8"  # Encoding of the .env file
        extra = 'allow'           # Allow extra fields in the settings


# Create a global instance of the settings
config = Settings()
