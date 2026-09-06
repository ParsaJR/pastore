from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from app.dependencies.admin import ProtectedRouteDep
from app.dependencies.database import CacheDep
from app.models.pasted import Duration, PastedCreate, PastedPublic
from app.service.pastedService import PastedServiceDep
from fastapi import APIRouter, Query

router = APIRouter(
    tags=["Pasted: Public routes"],
)

@router.get("/pastes/all", status_code=200)
async def get_all_pastes(
        admin: ProtectedRouteDep,
        pasted_service: PastedServiceDep,
        page: int = Query(1, ge=1),
        page_size: int = Query(10,ge=1),
        ):

    items = pasted_service.get_pastes(page,page_size)

    return items

@router.get("/pastes/{pasted_id}", response_model=PastedPublic, status_code=200)
async def get_pasted_by_id(pasted_id: int, pasted_service: PastedServiceDep):
    pasted_item = pasted_service.get_pasted_by_id(pasted_id)
    return pasted_item


@router.get("/pastes", response_model=PastedPublic, status_code=200)
async def get_pasted_by_shortcode(
        shortcode: str,
        pasted_service: PastedServiceDep,
        cache: CacheDep,
):
    cache_key = f"paste_code:{shortcode}"

    cached = await cache.get(cache_key)

    if cached:
        return PastedPublic.model_validate_json(cached)


    pasted_item = pasted_service.get_pasted_by_shortcode(shortcode)


    if pasted_item is None:
         raise HTTPException(status_code=404, detail="Paste not found")

    # For some reason, i can't directly serialize the "pasted_item" to json.
    # https://stackoverflow.com/questions/77637278/sqlalchemy-model-to-json
    pasted_public = PastedPublic.model_validate(pasted_item)

    # Only save the paste content if it wasn't a one_time kind.
    if not pasted_item.is_one_time:
        await cache.set(cache_key, pasted_public.model_dump_json(), 3600)

    return pasted_public


@router.post("/pastes", response_model=PastedPublic, status_code=201)
async def create_pasted(p: PastedCreate, pasted_service: PastedServiceDep):
    pasted_item = pasted_service.create_pasted(p)
    return pasted_item


