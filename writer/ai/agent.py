"""
Agent Module

This module defines the Agent class which is responsible for processing content
through language models with specific templates and system messages.
"""
from typing import Type, TypeVar
from pydantic import BaseModel
import logging

from writer.model import AgentInput
from writer.config import config
from writer.ai import get_llm_model, LLMProvider, infer

# Type variable for output model types
OutputType = TypeVar('OutputType', bound=BaseModel)

# Configure module logger
logger = logging.getLogger(__name__)


class Agent:
    """
    Generic agent that can be used for different types of content generation.
    
    This class handles the configuration and execution of content generation
    using language models with specific templates and system messages.
    """
    def __init__(
        self,
        template: str,
        system_message: str,
        output_model: Type[OutputType] = BaseModel,
        llm_provider: LLMProvider = LLMProvider(config.LLM_PROVIDER),
        model_name: str = config.LLM_MODEL
    ):
        """
        Initialize a new Agent instance.
        
        Args:
            template: The prompt template to use for content generation
            system_message: The system message to set context for the LLM
            output_model: The Pydantic model to use for output validation (default: BaseModel)
            llm_provider: The LLM provider to use (default: from config)
            model_name: The model name to use (default: from config)
        """
        self.output_model = output_model
        self.template = template
        self.system_message = system_message
        # Initialize the language model based on the provider and model name
        self.llm = get_llm_model(provider=llm_provider, model_name=model_name)
    
    def process(self, content: AgentInput) -> str:
        """
        Process the input content and generate output using the configured LLM.
        
        Args:
            content: The input content to process
            
        Returns:
            The generated content as a string
            
        Raises:
            Exception: If an error occurs during processing
        """
        try:
            # Use the infer function to process the content through the LLM
            result = infer(
                self.llm, 
                content.article_content, 
                content.target_audience, 
                self.template, 
                system_message=self.system_message
            )
            return result
        except Exception as e:
            logger.error(f"Error in agent processing: {str(e)}")
            raise

    @classmethod
    def create_blog_agent(
        cls,
        llm_provider: LLMProvider = LLMProvider(config.LLM_PROVIDER),
        model_name: str = config.LLM_MODEL
    ) -> 'Agent':
        """
        Factory method to create a blog content writer agent.
        
        Creates an agent configured with the appropriate template and system message
        for generating blog content.
        
        Args:
            llm_provider: The LLM provider to use (default: from config)
            model_name: The model name to use (default: from config)
            
        Returns:
            A configured Agent instance for blog content generation
        """
        from writer.ai.template import TEMPLATE, BLOG_SYSTEM_MESSAGE
        
        return cls(
            template=TEMPLATE,
            system_message=BLOG_SYSTEM_MESSAGE,
            llm_provider=llm_provider,
            model_name=model_name
        )
    
    @classmethod
    def create_x_agent(
        cls,
        llm_provider: LLMProvider = LLMProvider(config.LLM_PROVIDER),
        model_name: str = config.LLM_MODEL
    ) -> 'Agent':
        """
        Factory method to create an X (Twitter) content writer agent.
        
        Creates an agent configured with the appropriate template and system message
        for generating X (Twitter) content.
        
        Args:
            llm_provider: The LLM provider to use (default: from config)
            model_name: The model name to use (default: from config)
            
        Returns:
            A configured Agent instance for X content generation
        """
        from writer.ai.template import TEMPLATE, X_SYSTEM_MESSAGE
        
        return cls(
            template=TEMPLATE,
            system_message=X_SYSTEM_MESSAGE,
            llm_provider=llm_provider,
            model_name=model_name
        )

    @classmethod
    def create_linkedin_agent(
        cls,
        llm_provider: LLMProvider = LLMProvider(config.LLM_PROVIDER),
        model_name: str = config.LLM_MODEL
    ) -> 'Agent':
        """
        Factory method to create a LinkedIn content writer agent.
        
        Creates an agent configured with the appropriate template and system message
        for generating LinkedIn content.
        
        Args:
            llm_provider: The LLM provider to use (default: from config)
            model_name: The model name to use (default: from config)
            
        Returns:
            A configured Agent instance for LinkedIn content generation
        """
        from writer.ai.template import TEMPLATE, LINKEDIN_SYSTEM_MESSAGE
        
        return cls(
            template=TEMPLATE,
            system_message=LINKEDIN_SYSTEM_MESSAGE,
            llm_provider=llm_provider,
            model_name=model_name
        )
