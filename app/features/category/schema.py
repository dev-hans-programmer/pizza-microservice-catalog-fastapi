from pydantic import BaseModel
from enum import Enum


class PriceType(str, Enum):
    BASE = 'base'
    ADDITIONAL = 'additonal'


class WidgetType(str, Enum):
    SWITCH = 'switch'
    RADIO = 'radio'


class PriceConfigurationBase(BaseModel):
    key: str
    price_type: PriceType
    available_options: list[str]


class AttributeBase(BaseModel):
    name: str
    widget_type: WidgetType
    available_options: list[str]
    default_value: str | None | int | float


class CategoryBase(BaseModel):
    name: str


class PriceConfigurationCreate(PriceConfigurationBase):
    pass


class AttributeCreate(AttributeBase):
    pass


class CategoryCreate(CategoryBase):
    price_configurations: list[PriceConfigurationCreate]
    attributes: list[AttributeCreate]


class PriceConfigurationRead(PriceConfigurationBase):
    id: int


class AttributeRead(AttributeBase):
    id: int


class CategoryRead(CategoryBase):
    id: int
    price_configurations: list[PriceConfigurationRead]
    attributes: list[AttributeRead]
