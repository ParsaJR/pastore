from datetime import datetime, timedelta, timezone

from sqlmodel import select

from app.db import get_session
from app.models.pasted import Pasted


def delete_expired_pastes(days: int = 20) -> int:
    """Hard deletes the expired pastes"""
    with next(get_session()) as session:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)

        statement = select(Pasted).where(Pasted.created_at < cutoff)
        candidates = session.exec(statement).all()

        for paste in candidates:
            session.delete(paste)

        session.commit()

        return len(candidates)


if __name__ == "__main__":
    deleted = delete_expired_pastes()
    print(f"Done. Deleted {deleted} rows.")
