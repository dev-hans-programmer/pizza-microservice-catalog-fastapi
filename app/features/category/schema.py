from pydantic import BaseModel, Field, field_validator, ConfigDict, model_validator
from enum import Enum
from typing import Union


class PriceType(str, Enum):
    BASE = 'base'
    ADDITIONAL = 'additonal'


class WidgetType(str, Enum):
    SWITCH = 'switch'
    RADIO = 'radio'


class PriceConfigurationBase(BaseModel):
    key: str = Field(..., min_length=1, description='Unique key for price config')
    price_type: PriceType = Field(..., description='Either base or additional')
    available_options: list[str] = Field(
        ..., min_length=1, description='Atleast one option is required'
    )

    # if we provide " "(with space) then logic will fire off
    @field_validator('key')
    def validate_key(cls, v):
        if not v.strip():
            raise ValueError('key cannot be empty')
        return v

    @field_validator('available_options')
    def validate_available_options(cls, v):
        if any(not opt.strip() for opt in v):
            raise ValueError('Each available option must be non-empty')
        return v


class AttributeBase(BaseModel):
    name: str = Field(..., min_length=1, description='Attribute name is required')
    widget_type: WidgetType = Field(
        ..., description="widgetType must be either 'switch' or 'radio'"
    )
    available_options: list[str] = Field(
        ..., min_length=1, description='At least one available option is required'
    )
    default_value: Union[str, int, float, bool, None] = Field(
        ..., description='defaultValue is required (string | number | boolean | null)'
    )

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('attribute name cannot be empty')
        return v

    @model_validator(mode='after')  # runs for entire model after field validator
    # anyway this is reduntant now as we have required option for avalable_option
    # but in future if we need to just check based on widget_type
    # then this is useful
    def check_widget_type_logic(self):
        if self.widget_type == WidgetType.RADIO and not self.available_options:
            raise ValueError('Radio widget must have at least one available option')
        return self


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, description='Category name is required')


class PriceConfigurationCreate(PriceConfigurationBase):
    pass


class AttributeCreate(AttributeBase):
    pass


class CategoryCreate(CategoryBase):
    price_configurations: list[PriceConfigurationCreate] = Field(
        ..., min_length=1, description='At least one config is needed'
    )
    attributes: list[AttributeCreate] = Field(
        ..., min_length=1, description='At least one attribute is required'
    )

    @field_validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Category name cannot be empty')
        return v

    @field_validator('price_configurations')
    def validate_price_config_unique_keys(cls, v):
        keys = [cfg.key for cfg in v]
        if len(keys) != len(set(keys)):
            raise ValueError('Duplicate keys are not allowed in price_configurations')
        return v

    model_config = ConfigDict(from_attributes=True)


class PriceConfigurationRead(PriceConfigurationBase):
    id: int


class AttributeRead(AttributeBase):
    id: int


class CategoryRead(CategoryBase):
    id: int
    price_configurations: list[PriceConfigurationRead]
    attributes: list[AttributeRead]
