"""Validar token de GitHub y obtener datos del usuario."""
from github import Github, GithubException, Auth


class GitHubAuth:
    @staticmethod
    def validate_token(token: str):
        if not token or not token.strip():
            raise ValueError("Token vacio")

        token = token.strip()
        if not (token.startswith("ghp_") or token.startswith("github_pat_")):
            raise ValueError("Formato de token invalido (debe empezar con ghp_ o github_pat_)")

        try:
            gh = Github(auth=Auth.Token(token))
            user = gh.get_user()
            return {
                "login": user.login,
                "name": user.name or user.login,
                "avatar": user.avatar_url or "",
                "token": token,
            }
        except GithubException as e:
            msg = e.data.get("message", str(e)) if e.data else str(e)
            raise ValueError(f"Token invalido: {msg}")
        except Exception as e:
            raise ValueError(f"Error: {e}")