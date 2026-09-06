# All the Dependencies that can be used in the project, Liberally.
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from app import db
from app.core.cache.cache_interface import Cache

# Provides the orm capabilities to the entire app.
SessionDep = Annotated[Session,Depends(db.get_session)]

# Provides the configured redis client.
CacheDep = Annotated[Cache,Depends(db.get_cache)]
