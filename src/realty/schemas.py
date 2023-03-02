from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Status(BaseModel):
    id: int
    name: str


class LinkCreate(BaseModel):
    id: Optional[int]
    link: str
    status: Optional[Status]
    comment: Optional[str]
    created_ad: datetime


class LinkUpdate(BaseModel):
    status_id: int
    comment: Optional[str]


class ViewLinks(BaseModel):
    status: str
    data: List[LinkCreate]
    details: str | None = None


class Image(BaseModel):
    name: str
    url: str


class RegionBase(BaseModel):
    label: str


class RegionCreate(RegionBase):
    pass


class RegionUpdate(RegionBase):
    pass


class AddOkey(BaseModel):
    status: str
    data: Optional[str] = None
    message: str


class RegionRead(RegionBase):
    id: int

    class Config:
        orm_mode = True


class SettlemenTypeBase(BaseModel):
    label: str


class SettlemenTypeCreate(SettlemenTypeBase):
    pass


class SettlemenTypeUpdate(SettlemenTypeBase):
    pass


class SettlemenTypeRead(SettlemenTypeBase):
    id: int

    class Config:
        orm_mode = True


class DistrictBase(BaseModel):
    label: str
    region_id: int


class DistrictCreate(DistrictBase):
    pass


class DistrictUpdate(DistrictBase):
    pass


class DistrictRead(DistrictBase):
    id: int

    class Config:
        orm_mode = True


class SettlementBase(BaseModel):
    label: str
    region_id: int
    district_id: int
    settlement_types_id: int


class SettlementCreate(SettlementBase):
    pass


class SettlementUpdate(SettlementBase):
    pass


class SettlementRead(SettlementBase):
    id: int

    class Config:
        orm_mode = True


class HomeBase(BaseModel):
    title: str
    description: str
    status: bool
    region_id: int
    district_id: int
    settlement_id: int
    full_adress: str
    main_image: str
    video_zen: str = None
    video_rutube: str = None
    link_to_ads: str
    price: int
    area_of_house: int
    plot_area: int
    bathroom_in_house: bool
    gaz: bool


class HomeCreate(HomeBase):
    pass


class HomeUpdate(HomeBase):
    pass


class HomeRead(HomeBase):
    id: int
    created_at: str
    updated_at: str
    user_id: int
    region: RegionRead
    district: DistrictRead
    settlement: SettlementRead

    class Config:
        orm_mode = True


class HomeInResponse(BaseModel):
    count: int
    items: List[HomeRead]

    class Config:
        orm_mode = True
