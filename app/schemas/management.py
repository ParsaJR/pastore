from typing import Sequence, TypedDict
from pydantic.dataclasses import dataclass
from app.models.pasted import Pasted


@dataclass
class ExpiryDuration():
    name: str
    code: str

@dataclass
class APICapabilities():
    """Used to inform the clients about the available api capabilities."""
    expiry_durations: list[ExpiryDuration]

class PastedPublicDict(TypedDict):
    items: Sequence[Pasted]
    total_items: int
    current_page: int
    page_size: int
    total_pages: int
