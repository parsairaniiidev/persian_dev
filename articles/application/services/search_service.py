# application/services/search_service.py
from typing import List
from dependency_injector.wiring import inject, Provide
from articles.application.interfaces.services.search_service import SearchResult
from domain.repositories.search_log_repository import SearchLogRepository
from domain.entities.search_log import SearchLog

class SearchService:
    @inject
    def __init__(
        self,
        search_log_repo: SearchLogRepository = Provide['repository.search_log_repository']
    ):
        self._search_log_repo = search_log_repo
    
    def perform_search(self, query: str, user_id: str = None) -> List[SearchResult]:
        # Your search logic here...
        results = [...]  # Get search results
        
        # Log the search
        search_log = SearchLog(
            query=query,
            user_id=user_id,
            metadata={
                'result_count': len(results),
                'source': 'web'
            }
        )
        self._search_log_repo.log_search(search_log)
        
        return results