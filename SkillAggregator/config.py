from dataclasses import dataclass

@dataclass
class Config:
    db_path: str = "learning_analytics_database.db"
    sqlite_path: str = "sqlite:///learning_analytics_database.db"
    learning_model: str = "claude-3-sonnet-20240229"
    api_key: str = ""
    cache_enabled: bool = True
    cache_dir: str = ".cache/learning_analytics"
    cache_ttl: int = 86400  # Cache TTL in seconds (24 hours)

class ConfigError(Exception):
    """Custom exception for configuration errors"""
    pass 