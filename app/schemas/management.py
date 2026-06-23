from pydantic.dataclasses import dataclass


@dataclass
class ExpiryDuration():
    name: str
    code: str

@dataclass
class APICapabilities():
    """Used to inform the clients about the available options."""
    expiry_durations: list[ExpiryDuration]

@dataclass
class APIBranding():
    """Used to inform the clients about the available options."""
    app_name: str
    support_email: str
    privacy_policy: str
