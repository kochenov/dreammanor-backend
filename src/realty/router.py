import shutil
from typing import List, Dict, Union

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from auth.base_config import current_user
from auth.schemas import UserRead
from database import get_async_session
from realty.models import link, Link, Status, Home, Region, Districts, Settlements, SettlementType
from realty.schemas import LinkCreate, LinkUpdate, Image, RegionCreate, RegionRead, RegionBase, AddOkey, DistrictRead, \
    DistrictCreate, SettlementRead, SettlementCreate, SettlemenTypeCreate, SettlemenTypeRead, HomeRead, HomeCreate

router = APIRouter(
    prefix="/realty",
    tags=["Realty"]
)


@router.post("/upload-images/")
async def upload_images(images: List[UploadFile] = File(...)):
    uploaded_images = []
    for image in images:
        file_location = f"files/images/{image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        uploaded_images.append(Image(name=image.filename, url=file_location))
    return uploaded_images


# @app.post("/upload-images/")
# async def upload_images(images: List[UploadFile] = File(...)):
#     uploaded_images = []
#     for image in images:
#         file_location = f"images/{image.filename}"
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
#         uploaded_images.append({"name": image.filename, "url": file_location})
#     return {"uploaded_images": uploaded_images}


# @router.post("/upload")
# async def create_upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     with open(f"images/{file.filename}", "wb") as f:
#         f.write(contents)
#     return {"filename": file.filename}


@router.get("/links")
async def get_links_to_ads(limit: int = 1, offset: int = 0,
                           status_id: int = 0,
                           session: AsyncSession = Depends(get_async_session)):
    """Список ссылок на объявление"""
    try:
        order = Link.id.desc()
        query = select(Link).where(Link.status_id == status_id).options(selectinload(Link.status)).order_by(
            order).offset(
            offset).limit(limit)
        result = await session.execute(query)
        links = result.scalars().all()
        return {
            "status": "success",
            "data": links,
            "details": str(len(links))
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/links-status")
async def get_links_status_to_ads(session: AsyncSession = Depends(get_async_session)):
    """Список статусов ссылок"""
    try:
        query = select(Status)
        result = await session.execute(query)
        status = result.scalars().all()
        return {
            "status": "success",
            "data": status,
            "details": str(len(status))
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/links/new")
async def add_link_to_ads(new_link: LinkCreate, session: AsyncSession = Depends(get_async_session)):
    """Записать новую ссылку"""
    stmt = insert(link).values(**new_link.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/links/edit/{link_id}")
async def update_link_to_ads(link_id: int, edit_link: LinkUpdate, session: AsyncSession = Depends(get_async_session)):
    """Изменение ссылки"""
    stmt = update(Link).where(Link.id == link_id).values(**edit_link.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get("/houses")
async def get_house_list(limit: int = 1, offset: int = 0,
                         status: bool = False,
                         session: AsyncSession = Depends(get_async_session)):
    """Список объявлений"""
    try:
        order = Home.id.desc()
        query = select(Home).where(Home.status == status).order_by(
            order).offset(
            offset).limit(limit)
        result = await session.execute(query)
        links = result.scalars().all()
        return {
            "status": "success",
            "data": links,
            "message": str(len(links))
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "message": None
        })


# Regions
@router.post("/regions/", response_model=AddOkey)
async def create_region(region: RegionCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Region).values(**region.dict(exclude_unset=True))
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "message": "Новый регион успешно добавлен"
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "message": "Регион с таким именем уже существует"
        })


@router.get("/regions/", response_model=Dict[str, Union[str, List[RegionRead]]])
async def read_regions(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    query = select(Region).offset(skip).limit(limit)
    # regions = session.query(Region).offset(skip)
    result = await session.execute(query)
    regions = result.scalars().all()
    if not regions:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "message": "Список регионов пуст. Добавь новый регион"
        })
    return {
        "status": "success",
        "data": regions,
        "message": "Получен список регионов"
    }


@router.get("/districts/{region_id}", response_model=Dict[str, Union[str, List[DistrictRead]]])
async def read_districts(region_id: int, skip: int = 0, limit: int = 100,
                         session: AsyncSession = Depends(get_async_session)):
    query = select(Districts).where(Districts.region_id == region_id).offset(skip).limit(limit)
    # regions = session.query(Region).offset(skip)
    result = await session.execute(query)
    districts = result.scalars().all()

    if not districts:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "message": "Нет записей! Добавьте новый район"
        })
    return {
        "status": "success",
        "data": districts,
        "message": "Получен список районов"
    }


@router.post("/district/", response_model=AddOkey)
async def create_region(region: DistrictCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Districts).values(**region.dict(exclude_unset=True))
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "message": "Новый район успешно добавлен"
        }
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "message": "Район с таким именем уже существует"
        })


@router.get("/settlements/{region_id}/{district_id}/{settlement_type_id}",
            response_model=Dict[str, Union[str, List[SettlementRead]]])
async def read_settlements(region_id: int, district_id: int, settlement_type_id: int, skip: int = 0, limit: int = 100,
                           session: AsyncSession = Depends(get_async_session)):
    query = select(Settlements).filter(Settlements.region_id == region_id, Settlements.district_id == district_id,
                                       Settlements.settlement_types_id == settlement_type_id).offset(skip).limit(limit)
    result = await session.execute(query)
    settlements = result.scalars().all()

    if not settlements:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "message": "Нет записей! Добавьте новое поселение"
        })
    return {
        "status": "success",
        "data": settlements,
        "message": "Получен список поселений"
    }


@router.post("/settlement/", response_model=AddOkey)
async def create_settlement(settlement: SettlementCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Settlements).values(**settlement.dict(exclude_unset=True))
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "message": "Новое поселение успешно добавлено"
        }
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "message": "Поселение с таким именем уже существует"
        })


@router.post("/settlement-type/", response_model=AddOkey)
async def create_settlement_type(settlement_type: SettlemenTypeCreate,
                                 session: AsyncSession = Depends(get_async_session)):
    stmt = insert(SettlementType).values(**settlement_type.dict(exclude_unset=True))
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "message": "Новый тип успешно добавлен"
        }
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "message": "Тип поселения с таким именем уже существует"
        })


@router.get("/settlement-type/", response_model=Dict[str, Union[str, List[SettlemenTypeRead]]])
async def read_settlement_types(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    query = select(SettlementType).offset(skip).limit(limit)
    # regions = session.query(Region).offset(skip)
    result = await session.execute(query)
    settlement_types = result.scalars().all()
    if not settlement_types:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "message": "Список типов поселений пуст. Добавь новый тип поселения"
        })
    return {
        "status": "success",
        "data": settlement_types,
        "message": "Получен список регионов"
    }


@router.get("/all-homes/", response_model=Dict[str, Union[str, List[HomeRead]]])
async def read_all_homes(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_async_session)):
    query = select(Home).offset(skip).limit(limit)
    result = await session.execute(query)
    regions = result.scalars().all()
    if not regions:
        raise HTTPException(status_code=404, detail={
            "status": "error",
            "data": None,
            "message": "Объявлений о продаже домов пока ещё нет"
        })
    return {
        "status": "success",
        "data": regions,
        "message": "Получен список объявлений"
    }


# @router.post("/home/", response_model=AddOkey)
# async def create_home(home: HomeCreate, user: UserRead = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(Home).values(**home.dict(exclude_unset=True),user_id = user.id)
#     try:
#         await session.execute(stmt)
#         await session.commit()
#         return {
#             "status": "success",
#             "data": None,
#             "message": "Объявление успешно добавлено"
#         }
#     except IntegrityError as e:
#         print(e)
#         raise HTTPException(status_code=400, detail={
#             "status": "error",
#             "data": None,
#             "message": "Такое объявление уже есть:Измените заголовок"
#         })


@router.post("/home/", response_model=AddOkey)
async def create_home(home: HomeCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Home).values(**home.dict(exclude_unset=True), user_id=1)
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "message": "Объявление успешно добавлено"
        }
    except IntegrityError as e:
        print(e)
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "message": "Такое объявление уже есть:Измените заголовок"
        })
