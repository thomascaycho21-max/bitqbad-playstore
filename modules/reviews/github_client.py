"""Cliente GitHub Issues para reseñas."""
import os
from github import Github, GithubException


class GitHubReviewsClient:
    def __init__(self, token=None, repo_name=None, label=None):
        self.token = (token or os.getenv("GITHUB_TOKEN", "")).strip()
        self.repo_name = (repo_name or os.getenv("GITHUB_REPO", "")).strip()
        self.label = (label or os.getenv("GITHUB_REVIEW_LABEL", "review")).strip()

        self.error = None
        self.repo = None
        self.enabled = False

        # Validaciones
        if not self.token:
            self.error = "Falta GITHUB_TOKEN en .env"
            return
        if not self.token.startswith(("ghp_", "github_pat_")):
            self.error = "El token no empieza por ghp_ o github_pat_"
            return
        if not self.repo_name:
            self.error = "Falta GITHUB_REPO en .env"
            return
        if "/" not in self.repo_name:
            self.error = (
                f"GITHUB_REPO='{self.repo_name}' debe ser 'usuario/repositorio'. "
                "Ejemplo: thomas-dev/bitqbad-reviews"
            )
            return

        # Intentar conectar
        try:
            gh = Github(self.token)
            self.repo = gh.get_repo(self.repo_name)
            self.enabled = True
        except GithubException as e:
            msg = e.data.get("message", str(e)) if e.data else str(e)
            self.error = f"GitHub: {msg} (repo: {self.repo_name})"
        except Exception as e:
            self.error = f"Error inesperado: {e}"

    def ensure_label(self):
        if not self.enabled:
            return
        try:
            self.repo.get_label(self.label)
        except GithubException:
            try:
                self.repo.create_label(
                    name=self.label,
                    color="7C4DFF",
                    description="Reseñas de BitQbad PlayStore"
                )
            except GithubException:
                pass

    def create_review(self, app_id, title, body, rating, user="anon"):
        if not self.enabled:
            raise RuntimeError(self.error or "GitHub no configurado")

        import json
        meta = json.dumps({"rating": rating, "user": user}, ensure_ascii=False)
        full_body = (
            f"<!-- meta: {meta} -->\n\n"
            f"**App:** `{app_id}`\n"
            f"**Rating:** {'⭐' * max(0, min(5, rating))} ({rating}/5)\n\n"
            f"---\n\n{body}\n"
        )
        return self.repo.create_issue(
            title=f"review:{app_id} :: {title}",
            body=full_body,
            labels=[self.label],
        )

    def list_reviews(self, app_id=None):
        if not self.enabled:
            return []
        try:
            issues = self.repo.get_issues(state="all", labels=[self.label])
            result = []
            for issue in issues:
                if issue.pull_request:
                    continue
                if app_id and f"review:{app_id}" not in (issue.title or ""):
                    continue
                result.append(issue)
            return result
        except GithubException:
            return []