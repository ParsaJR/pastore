from sqlmodel import Session,select
from app import db
from app.core import logs,config
from app.models.management import Admin, AdminCreate
from app.service.adminService import AdminService


def create_super_admin():
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
                plain_password="admin1234",
                repeat_password="admin1234",
                email="admin@admin.com",
            )

            admin_service.create_admin(admin)

            return True

        return None
