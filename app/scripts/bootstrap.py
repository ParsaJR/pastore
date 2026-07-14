import logging

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app import db
from app.core import config, logs
from app.models.management import Admin, AdminCreate
from app.service.adminService import AdminService


def ensure_an_admin_exists() -> bool:
    with Session(db.engine) as session:
        admin_service = AdminService(session)

        anyAdminExists = admin_service.is_any_admin_exists()
        if not anyAdminExists:
            password = config.settings.initial_admin_password
            if password is None:
                raise RuntimeError(
                    "No admin exists and PASTORE_INITIAL_ADMIN_PASSWORD is not set."
                )

            admin = AdminCreate(
                username="admin",
                plain_password=password,
                repeat_password=password,
                email="admin@admin.com",
            )

            try:
                admin_service.create_admin(admin)
                return True
            except IntegrityError:
                # The integrity error here generally means, this instance has lost the race for creating the initial admin.
                return False

        return False

def run():
    log = logs.get_logger()
    log.info("Running the boostrap tasks...")

    if ensure_an_admin_exists():
        log.info("Initial admin account has been created.")


    log.info("Running the boostrap tasks...Done")

if __name__ == "__main__":
    run()
