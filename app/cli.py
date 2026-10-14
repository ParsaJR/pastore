
# app/cli.py

import argparse
from getpass import getpass

from sqlmodel import select

from app.core import security
from app.db import get_session
from app.models.management import Admin


def reset_password(username: str) -> None:
    password = getpass("New password: ")
    confirmation = getpass("Confirm new password: ")

    if password != confirmation:
        raise SystemExit("Passwords do not match.")

    if len(password) < 6:
        raise SystemExit("Password must be at least 6 characters.")

    with next(get_session()) as session:
        user = session.exec(
            select(Admin).where(Admin.username == username)
        ).first()

        if user is None:
            raise SystemExit(f"User {username!r} not found.")

        user.hashed_password = security.get_password_hash(password)
        session.add(user)
        session.commit()

    print(f"Password updated for {username!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    reset_parser = subparsers.add_parser("reset-password")
    reset_parser.add_argument("username")

    args = parser.parse_args()

    if args.command == "reset-password":
        reset_password(args.username)


if __name__ == "__main__":
    main()
