"""
Search Engine Base Module

This module defines the abstract base class for all search engine implementations.
It provides a common interface for different search engine providers.
"""
from abc import ABC, abstractmethod
from typing import List

from writer.model import SearchResult


class SearchEngine(ABC):
    """
    Abstract base class for all search engines.
    
    This class defines the interface that all search engine implementations must follow.
    Concrete implementations should inherit from this class and implement the search method.
    """

    @abstractmethod
    def search(self, query: str) -> List[SearchResult]:
        """
        Search for the given query and return a list of search results.
        
        Args:
            query: The search query string
            
        Returns:
            A list of SearchResult objects containing the search results
        """
        pass
