from app.dependencies.admin import ProtectedRouteDep
from app.dependencies.database import CacheDep
from app.models.management import AdminPasswordChange, BrandingBase
from app.routers.auth import AdminServiceDep
from fastapi import APIRouter, HTTPException, Response
from app.core import security

from app.schemas.management import APICapabilities
from app.service.pastedService import PastedServiceDep

router = APIRouter(
    tags=["Pastore: Management routes"],
    prefix="/management",
)


@router.get("/what-is-available", response_model=APICapabilities, status_code=200)
def api_capabilities(admin_service: AdminServiceDep, response: Response):
    response.headers["Cache-Control"] = "public, max-age=30"
    return admin_service.get_api_capabilities()

@router.get("/branding", response_model=BrandingBase, status_code=200)
def branding(admin_service: AdminServiceDep, response: Response):
    response.headers["Cache-Control"] = "public, max-age=86400"
    branding = admin_service.get_branding()

    return branding


@router.put("/branding", status_code=201)
async def put_branding(
        admin_service: AdminServiceDep, admin: ProtectedRouteDep,  b: BrandingBase
):
    admin_service.put_branding(b)





@router.delete("/pastes/{paste_id}", status_code=204)
async def delete_paste(
        paste_id: int, pasted_service: PastedServiceDep, admin: ProtectedRouteDep, cache: CacheDep,
):
    pasted = pasted_service.delete_paste_by_id(paste_id)
    if not pasted:
        raise HTTPException(status_code=404, detail="Paste not found.")

    await cache.delete(key=f"paste_code:{pasted.shortcode}")

@router.get("/pastes/restore/{paste_id}", status_code=204)
async def restore_paste(
    paste_id: int, pasted_service: PastedServiceDep, admin: ProtectedRouteDep
):
    pasted = pasted_service.restore_paste_by_id(paste_id)
    if not pasted:
        raise HTTPException(status_code=404, detail="Paste not found.")


@router.post("/change-password", status_code=204)
async def change_password(
    admin_service: AdminServiceDep, admin: ProtectedRouteDep, body: AdminPasswordChange
):
    """Changes the super admin's password"""

    admin_service.change_password(
        admin.username, body.current_password, body.new_password
    )
