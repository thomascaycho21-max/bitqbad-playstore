"""Persistencia de monedas en un repo de GitHub (archivo JSON)."""
import json
import os
import base64
from github import Github, GithubException


class GitHubWallet:
    """Guarda cada usuario como archivo wallets/<user>.json en un repo."""

    def __init__(self, token=None, repo_name=None, folder="wallets"):
        self.token = (token or os.getenv("GITHUB_TOKEN", "")).strip()
        self.repo_name = (repo_name or os.getenv("GITHUB_COINS_REPO", "")).strip()
        self.folder = folder
        self.enabled = False
        self.repo = None
        self.error = None

        if not self.token:
            self.error = "Falta GITHUB_TOKEN en .env"
            return
        if not self.repo_name:
            self.error = "Falta GITHUB_COINS_REPO en .env (ej: usuario/bitqbad-coins)"
            return
        if "/" not in self.repo_name:
            self.error = f"GITHUB_COINS_REPO='{self.repo_name}' debe ser 'usuario/repo'"
            return

        try:
            gh = Github(self.token)
            self.repo = gh.get_repo(self.repo_name)
            self.enabled = True
        except GithubException as e:
            msg = e.data.get("message", str(e)) if e.data else str(e)
            self.error = f"GitHub: {msg}"

    def _path(self, user: str) -> str:
        safe = "".join(c for c in user if c.isalnum() or c in "-_") or "anon"
        return f"{self.folder}/{safe}.json"

    def load(self, user: str) -> dict | None:
        if not self.enabled:
            return None
        try:
            f = self.repo.get_contents(self._path(user))
            content = base64.b64decode(f.content).decode("utf-8")
            return json.loads(content)
        except GithubException:
            return None
        except Exception:
            return None

    def save(self, user: str, data: dict) -> bool:
        if not self.enabled:
            return False
        path = self._path(user)
        content = json.dumps(data, indent=2, ensure_ascii=False)
        try:
            try:
                existing = self.repo.get_contents(path)
                self.repo.update_file(
                    path=path,
                    message=f"update wallet {user}",
                    content=content,
                    sha=existing.sha,
                )
            except GithubException:
                self.repo.create_file(
                    path=path,
                    message=f"create wallet {user}",
                    content=content,
                )
            return True
        except Exception as e:
            print(f"[GitHubWallet] Error guardando: {e}")
            return False