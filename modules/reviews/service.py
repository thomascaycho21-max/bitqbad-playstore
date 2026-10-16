"""Servicio de reseñas: cache + GitHub."""
from typing import List
from .github_client import GitHubReviewsClient
from .models import Review


class ReviewsService:
    _instance = None

    def __new__(cls, *a, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.client = GitHubReviewsClient()
        if self.client.enabled:
            self.client.ensure_label()
        self._cache = {}
        self.enabled = self.client.enabled
        self.error = self.client.error

    def list_for(self, app_id: str, force: bool = False) -> List[Review]:
        if not self.enabled:
            return []
        if not force and app_id in self._cache:
            return self._cache[app_id]
        issues = self.client.list_reviews(app_id=app_id)
        reviews = [Review.from_issue(i) for i in issues]
        reviews.sort(key=lambda r: r.created_at, reverse=True)
        self._cache[app_id] = reviews
        return reviews

    def add(self, app_id, title, body, rating, user="anon"):
        if not self.enabled:
            raise RuntimeError(self.error or "GitHub no configurado")
        issue = self.client.create_review(app_id, title, body, rating, user)
        self._cache.pop(app_id, None)
        return issue

    def average_rating(self, app_id: str) -> float:
        reviews = self.list_for(app_id)
        if not reviews:
            return 0.0
        return sum(r.rating for r in reviews) / len(reviews)