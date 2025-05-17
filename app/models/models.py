from pydantic import BaseModel, Field, field_validator
import re

class PhoneAddressData(BaseModel):
    phone: str = Field(..., description="Номер телефона в формате 8XXXXXXXXXX")
    address: str = Field(..., min_length=5, max_length=500, description="Адрес пользователя")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not re.match(r'^8\d{10}$', v):
            raise ValueError('Телефон должен быть в формате 8XXXXXXXXXX')
        return v
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Адрес не может быть пустым')
        return v

class PhoneAddressUpdateData(BaseModel):
    address: str = Field(..., min_length=5, max_length=500, description="Новый адрес пользователя")
    
    @field_validator('address')
    @classmethod
    def validate_address(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Адрес не может быть пустым')
        return v

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Описание ошибки")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Статус сервиса")
    redis: str = Field(..., description="Статус подключения к Redis")
    
class SuccessResponse(BaseModel):
    status: str = Field("success", description="Статус операции")
    message: str = Field(..., description="Сообщение об успешном выполнении")