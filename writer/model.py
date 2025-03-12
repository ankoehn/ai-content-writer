"""
Data Models Module

This module defines the data models used throughout the application
using Pydantic for data validation and serialization.
"""
from pydantic import BaseModel


class AgentInput(BaseModel):
    """
    Input data model for AI agents.
    
    Attributes:
        article_content: The content to process (typically search results)
        target_audience: The target audience for the generated content
    """
    article_content: str = ""
    target_audience: str = ""


class SearchResult(BaseModel):
    """
    Model for search engine results.
    
    Attributes:
        title: The title of the search result
        content: The content/body of the search result
    """
    title: str
    content: str
