"""Modelo Review."""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    id: int
    app_id: str
    user: str
    rating: int
    title: str
    body: str
    created_at: str
    url: str = ""

    @classmethod
    def from_issue(cls, issue, app_id_prefix: str = "review:"):
        """Convierte un Issue de GitHub en Review.
        Formato del titulo: 'review:APP_ID :: TITULO'
        Body JSON: {rating, body, user}
        """
        title = issue.title or ""
        app_id = ""
        real_title = title
        if title.lower().startswith(app_id_prefix):
            rest = title[len(app_id_prefix):].strip()
            if "::" in rest:
                app_id, real_title = [p.strip() for p in rest.split("::", 1)]
            else:
                app_id = rest

        # Intentar leer metadata del body
        import json, re
        rating = 0
        user = issue.user.login if issue.user else "anon"
        body = issue.body or ""

        m = re.search(r"<!--\s*meta:\s*(\{.*?\})\s*-->", body, re.DOTALL)
        if m:
            try:
                meta = json.loads(m.group(1))
                rating = int(meta.get("rating", 0))
                user = meta.get("user", user)
                body = body.replace(m.group(0), "").strip()
            except Exception:
                pass

        return cls(
            id=issue.number,
            app_id=app_id,
            user=user,
            rating=rating,
            title=real_title,
            body=body,
            created_at=issue.created_at.isoformat() if issue.created_at else "",
            url=issue.html_url or "",
        )