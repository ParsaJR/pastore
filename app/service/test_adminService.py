# An Integration/Unit Test for the adminService.py.

import pytest
from sqlmodel import SQLModel, Session, StaticPool, create_engine

from app.models.management import AdminCreate, Branding, BrandingBase
from app.models.pasted import PastedExpiryDuration
from app.service.adminService import AdminService


# session_fixture yields a session that can be used for other tests.
# Presumably, we're cheating a little bit by using sqlite instead of
# postgresql. But it's better then nothing. In near future, i can consider using
# test-containers for real integration test.
@pytest.fixture(name="session")
def session_fixture():
    """Sets up the session for testing. Also Does the table creation."""

    # Using `StaticPool` will help us maintain a single in-memory database to
    # every test function.
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    # Create the database schema
    SQLModel.metadata.create_all(engine)

    # Add a sample expiry-duration.
    with Session(engine) as session:
        session.add(
            PastedExpiryDuration(
                name="1 day",
                code="oneDay",
                days=1,
            )
        )

        session.add(
            Branding(
                app_name="Old",
                app_description="Desc",
                support_email="old@example.com",
                privacy_policy="Old policy",
                message_of_the_day="Old msg",
            )
        )

        session.commit()

        yield session


@pytest.fixture(name="admin_service")
def admin_service(session):
    admin_service = AdminService(session)

    yield admin_service


def test_put_branding(admin_service: AdminService):
    updated = BrandingBase(
        app_name="New",
        app_description="Desc",
        support_email="new@example.com",
        privacy_policy="New policy",
        message_of_the_day="New msg",
    )

    result = admin_service.put_branding(updated)

    assert result.app_name == "New"
    assert result.support_email == "new@example.com"


def test_create_admin_and_authenticate(admin_service: AdminService):

    new_admin = AdminCreate(
        username="parsa",
        email="hi@proton.me",
        plain_password="123456abc", # "abc" is here to pass the pydantic validation logic.
        repeat_password="123456abc",
    )

    admin_service.create_admin(new_admin)


    retrieved_admin = admin_service.authenticate(username="parsa",password="123456abc")

    assert retrieved_admin.email == "hi@proton.me"
    
