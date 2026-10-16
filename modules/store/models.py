"""Modelo App."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class App:
    id: str
    name: str
    short_desc: str = ""
    long_desc: str = ""
    category: str = "Otros"
    version: str = "1.0.0"
    size_mb: float = 0.0
    rating: float = 0.0
    downloads: int = 0
    icon_color: str = "#7C4DFF"
    icon_emoji: str = "📦"
    platforms: List[str] = field(default_factory=list)
    download_url: str = ""
    repo_url: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "App":
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            short_desc=d.get("short_desc", ""),
            long_desc=d.get("long_desc", ""),
            category=d.get("category", "Otros"),
            version=d.get("version", "1.0.0"),
            size_mb=float(d.get("size_mb", 0)),
            rating=float(d.get("rating", 0)),
            downloads=int(d.get("downloads", 0)),
            icon_color=d.get("icon_color", "#7C4DFF"),
            icon_emoji=d.get("icon_emoji", "📦"),
            platforms=d.get("platforms", []),
            download_url=d.get("download_url", ""),
            repo_url=d.get("repo_url", ""),
        )

    def downloads_str(self) -> str:
        if self.downloads >= 1_000_000:
            return f"{self.downloads/1_000_000:.1f}M"
        if self.downloads >= 1_000:
            return f"{self.downloads/1_000:.1f}K"
        return str(self.downloads)
