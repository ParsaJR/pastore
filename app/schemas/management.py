from pydantic.dataclasses import dataclass


@dataclass
class ExpiryDuration():
    name: str
    code: str

@dataclass
class APICapabilities():
    """Used to inform the clients about the available api capabilities."""
    expiry_durations: list[ExpiryDuration]

@dataclass
class APIBranding():
    """Used to inform the clients about the service information e.g. the owner's email"""
    app_name: str
    support_email: str
    app_description: str
    privacy_policy: str
