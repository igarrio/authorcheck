from dataclasses import dataclass


@dataclass
class PixivDataForParsing:
    """Data container for Pixiv URL parsing parameters."""
    url: str
    meta_count: int
    link_type: str
    job_id: str
    target: str
