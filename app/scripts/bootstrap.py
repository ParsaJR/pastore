from app.core import logs
from app.utils.manage import create_super_admin


def run():
    log = logs.get_logger()
    log.info("Starting up the initial tasks...")
    log.info("Creating the super admin...")

    created = create_super_admin()

    if created:
        log.info("Initial super admin account has been created.")
    else:
        log.info("Initial admin already exists. skipping...")


if __name__ == "__main__":
    run()
