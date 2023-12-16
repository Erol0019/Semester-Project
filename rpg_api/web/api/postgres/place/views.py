from loguru import logger
from rpg_api.utils import dtos
from fastapi import Depends
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from pydantic import BaseModel, Field


router = APIRouter()


class PlaceFilterDTO(BaseModel):
    """Search DTO for Place."""

    search: str | None = Field(
        None,
        description="Search for places by name/description.",
    )


@router.get("", status_code=200)  # , dependencies=[Depends(get_current_user)])
async def get_places(
    daos: GetDAOs,
    filter_dto: PlaceFilterDTO = Depends(),
) -> dtos.DataListResponse[dtos.PlaceDTO]:
    """Get all places."""

    return dtos.DataListResponse(
        data=await daos.place.by_search(filter_dto.search)
        if filter_dto.search
        else [dtos.PlaceDTO.model_validate(c) for c in await daos.place.filter()]
    )


@router.post("", status_code=201)
async def create_place(
    input_dto: dtos.PlaceInputDTO,
    daos: GetDAOs,
) -> dtos.DefaultCreatedResponse:
    """Create place."""

    try:
        created_place_id = await daos.place.create(input_dto)
    except Exception as e:
        logger.exception(e)
        return dtos.DefaultCreatedResponse(
            message=str(e),
        )

    return dtos.DefaultCreatedResponse(
        data=created_place_id,
    )
