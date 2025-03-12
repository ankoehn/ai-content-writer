"""
Tavily Search Engine Module

This module implements the SearchEngine interface using the Tavily API.
It provides functionality to search for content using the Tavily search service.
"""
from typing import List

from tavily import TavilyClient

from writer.config import config
from writer.model import SearchResult
from writer.searchengine.engine import SearchEngine
from writer.utils.logging_config import get_logger

# Get logger for this module
logger = get_logger(__name__)


class TavilySearchEngine(SearchEngine):
    """
    Tavily search engine implementation.
    
    This class implements the SearchEngine interface using the Tavily API
    to perform web searches and retrieve relevant content.
    """

    def __init__(self):
        """
        Initialize the Tavily search engine with the API key from config.
        """
        logger.debug("Initializing TavilySearchEngine")
        self.client = TavilyClient(api_key=config.TAVILY_API_KEY)
        logger.info("TavilySearchEngine initialized successfully")

    def search(self, query: str) -> List[SearchResult]:
        """
        Search for the given query using Tavily API.
        
        Args:
            query: The search query string
            
        Returns:
            A list of SearchResult objects containing the search results
            
        Note:
            The search parameters are configured using the application settings
            from the config module.
        """
        logger.info(f"Searching for: '{query}'")
        logger.debug(f"Search parameters: depth={config.TAVILY_SEARCH_DEPTH}, "
                    f"topic={config.TAVILY_TOPIC}, max_results={config.TAVILY_MAX_RESULTS}")
        
        try:
            # Call the Tavily API with the configured parameters
            logger.debug("Calling Tavily API")
            response = self.client.search(
                query=query,
                search_depth=config.TAVILY_SEARCH_DEPTH,
                include_answer=config.TAVILY_INCLUDE_ANSWER,
                topic=config.TAVILY_TOPIC,
                include_raw_content=config.TAVILY_INCLUDE_RAW_CONTENT,
                max_results=config.TAVILY_MAX_RESULTS
            )
            
            # Process the response and convert to SearchResult objects
            results = []
            result_count = len(response.get("results", []))
            logger.info(f"Received {result_count} search results from Tavily API")
            
            for i, item in enumerate(response.get("results", [])):
                # Extract content from raw content if available, otherwise use snippet
                content = item.get("raw_content", item.get("content", ""))
                title = item.get("title", "")
                
                logger.debug(f"Processing result {i+1}/{result_count}: '{title[:50]}...' ({len(content)} chars)")
                
                results.append(SearchResult(
                    title=title,
                    content=content
                ))
            
            logger.info(f"Successfully processed {len(results)} search results")
            return results
            
        except Exception as e:
            logger.error(f"Error searching with Tavily API: {str(e)}", exc_info=True)
            raise
