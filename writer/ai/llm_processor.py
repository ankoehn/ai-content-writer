"""
LLM Processor Module

This module handles the processing of content through language models,
setting up prompts and handling the inference process.
"""
import logging

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Configure module logger
logger = logging.getLogger(__name__)


def infer(llm, article_content: str, target_audience: str, template, system_message: str = None):
    """
    Process content through a language model using the provided template and system message.
    
    Args:
        llm: The language model instance to use for inference
        article_content: The content to process (typically search results or article text)
        target_audience: The target audience for the generated content
        template: The prompt template to use for the human message
        system_message: Optional system message to set context for the LLM
        
    Returns:
        The generated content as a string, or None if an error occurred
    """
    logger.info(f"Starting inference with model: {str(llm)}")
    
    try:
        # Create a chat prompt template with system and human messages
        if not system_message:
            logger.warning("No system message provided, using empty string")
            system_message = ""
            
        # Create message templates for the chat prompt
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
        human_message_prompt = HumanMessagePromptTemplate.from_template(template)
        
        # Combine messages into a chat prompt and create processing sequence
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
        sequence = chat_prompt | llm

        # Prepare input values for the template
        input_values = {
            'article_content': article_content,
            'target_audience': target_audience
        }
        
        try:
            # Invoke the LLM with the prepared prompt and inputs
            llm_result = sequence.invoke(input_values)
            
            # Extract and return the content from the result
            result = llm_result.content                    
            return result
        except Exception as e:
            # Log errors that occur during LLM processing
            logger.error(f"LLM provider: {str(llm)}")
            logger.error(f"Error during LLM processing: {str(e)}")
            return None

    except Exception as e:
        # Log errors that occur during setup
        logger.error(f"Error setting up LLM pipeline: {str(e)}")
        return None
