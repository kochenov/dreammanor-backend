from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()

link = Table(
    "link",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("link", String(500), nullable=False, unique=True),
    Column("status_id", Integer, ForeignKey("status.id")),
    Column("comment", String(250), nullable=True),
    Column("created_ad", TIMESTAMP, default=datetime.utcnow),
)

status = Table(
    "status",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String(255), nullable=False),
)

region = Table(
    "regions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String(255), nullable=False, unique=True),
)

district = Table(
    "districts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String(255), nullable=False, unique=True),
    Column("region_id", Integer, ForeignKey("regions.id"))
)

settlement_types = Table(
    "settlement_types",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String(255), nullable=False, unique=True),
)

settlement = Table(
    "settlements",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("label", String(255), nullable=False),
    Column("region_id", Integer, ForeignKey("regions.id")),
    Column("district_id", Integer, ForeignKey("districts.id")),
    Column("settlement_types_id", Integer, ForeignKey("settlement_types.id"))
)

home = Table(
    "overview_of_houses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(255), nullable=False, unique=True),
    Column("description", String(5000), nullable=False),
    Column("status", Boolean, nullable=False),
    Column("region_id", Integer, ForeignKey("regions.id")),  # Область
    Column("district_id", Integer, ForeignKey("districts.id")),  # Районы
    Column("settlement_id", Integer, ForeignKey("settlements.id")),  # Поселения
    Column("user_id", Integer, nullable=False),
    Column("full_adress", String(500), nullable=False),
    Column("main_image", String(1000), nullable=False),
    Column("video_zen", String(1000), nullable=True),
    Column("video_rutube", String(1000), nullable=True),
    Column("link_to_ads", String(1000), nullable=False),
    Column("price", Integer, nullable=False),
    Column("area_of_house", Integer, nullable=False),  # площадь дома
    Column("plot_area", Integer, nullable=False),  # площадь участка
    Column("bathroom_in_house", Boolean, nullable=False),  # Туалет в доме
    Column("gaz", Boolean, nullable=False, default=False),  # Есть газ
    Column("created_ad", TIMESTAMP, default=datetime.utcnow),
)


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False)

    class Config:
        orm_mode = True


class Link(Base):
    __tablename__ = "link"
    id = Column(Integer, primary_key=True)
    link = Column(String(500), nullable=False, unique=True)
    status_id = Column(Integer, ForeignKey("status.id"))
    comment = Column(String(500), nullable=False)
    created_ad = Column(TIMESTAMP, default=datetime.utcnow)
    status = relationship("Status")

    class Config:
        orm_mode = True


class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False, unique=True)

    class Config:
        orm_mode = True


class Districts(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)  # Область

    class Config:
        orm_mode = True


class SettlementType(Base):
    __tablename__ = "settlement_types"
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False, unique=True)


class Settlements(Base):
    __tablename__ = "settlements"
    id = Column(Integer, primary_key=True)
    label = Column(String(255), nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey("regions.id"))  # Область
    district_id = Column(Integer, ForeignKey("districts.id"))  # Район
    settlement_types_id = Column(Integer, ForeignKey("settlement_types.id"))

    class Config:
        orm_mode = True


class Home(Base):
    __tablename__ = "overview_of_houses"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    description = Column(String(5000), nullable=False)
    status = Column(Boolean, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"))  # Область
    district_id = Column(Integer, ForeignKey("districts.id"))  # Районы
    settlement_id = Column(Integer, ForeignKey("settlements.id"))  # Поселения
    full_adress = Column(String(500), nullable=False)
    main_image = Column(String(1000), nullable=False)
    video_zen = Column(String(1000), nullable=True)
    video_rutube = Column(String(1000), nullable=True)
    link_to_ads = Column(String(1000), nullable=False)
    price = Column(Integer, nullable=False)
    area_of_house = Column(Integer, nullable=False)  # площадь дома
    plot_area = Column(Integer, nullable=False)  # площадь участка
    bathroom_in_house = Column(Boolean, nullable=False)  # Туалет в доме
    gaz = Column(Boolean, nullable=False, default=False)  # Есть газ
    created_ad = Column(TIMESTAMP, default=datetime.utcnow)
    region = relationship("Region")
    district = relationship("Districts")
    settlement = relationship("Settlements")
    user_id = Column(Integer, nullable=False)

    class Config:
        orm_mode = True
