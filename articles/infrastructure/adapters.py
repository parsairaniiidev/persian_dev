# articles/infrastructure/adapters/
# آداپتور برای Elasticsearch
class ElasticsearchSearchAdapter:
    def __init__(self, client):
        self.client = client
    
    def search_articles(self, query: str) -> list:
        # تبدیل query به فرمت Elasticsearch
        es_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"]
                }
            }
        }
        results = self.client.search(index="articles", body=es_query)
        return [hit['_source'] for hit in results['hits']['hits']]

# آداپتور برای Redis (مثال)
class RedisCacheAdapter:
    def __init__(self, redis_client):
        self.client = redis_client
    
    def get_article(self, article_id: str) -> dict:
        return self.client.get(f"article:{article_id}")