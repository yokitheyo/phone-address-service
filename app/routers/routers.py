from fastapi import APIRouter, Depends, Path, Query, status
from app.models.models import PhoneAddressData, SuccessResponse, PhoneAddressUpdateData
from app.services.services import RedisService
from app.services.interfaces import StorageInterface
from app.utils.logging import logger
from app.exceptions.service_exceptions import (
    handle_service_error, 
    handle_not_found_error, 
    handle_conflict_error, 
    handle_update_error
)

router = APIRouter(prefix="/contacts", tags=["Contacts"])

def get_storage_service() -> StorageInterface:
    return RedisService()

@router.get("/{phone}", response_model=dict, summary="Получение адреса по номеру телефона")
async def get_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    storage_service: StorageInterface = Depends(get_storage_service)
):
    logger.info(f"Запрос адреса для телефона: {phone}")
    address, success = await storage_service.get_address_by_phone(phone)
    
    if not success:
        handle_service_error("хранилища", "получении адреса", phone)
    
    if not address:
        handle_not_found_error("Адрес", phone)
    
    logger.info(f"Адрес для телефона {phone} успешно получен")
    return {"phone": phone, "address": address}

@router.post("/", response_model=SuccessResponse, summary="Создание новой записи")
async def create_phone_address(
    data: PhoneAddressData,
    storage_service: StorageInterface = Depends(get_storage_service)
):
    logger.info(f"Запрос на создание записи для телефона: {data.phone}")
    
    existing_address, success = await storage_service.get_address_by_phone(data.phone)
    
    if not success:
        handle_service_error("хранилища", "проверке существования телефона", data.phone)
    
    if existing_address:
        handle_conflict_error("Запись", data.phone)
    
    success = await storage_service.save_phone_address(data.phone, data.address)
    if not success:
        handle_update_error("данных", data.phone, "сохранении")
    
    logger.info(f"Запись для телефона {data.phone} успешно создана")
    return {"status": "success", "message": "Данные успешно сохранены"}

@router.put("/{phone}", response_model=SuccessResponse, summary="Полное обновление записи")
async def update_phone_address(
    phone: str = Path(..., description="Текущий номер телефона в формате 8XXXXXXXXXX"),
    data: PhoneAddressData = None,
    storage_service: StorageInterface = Depends(get_storage_service)
):
    logger.info(f"Запрос на обновление записи для телефона: {phone}")
    address, success = await storage_service.get_address_by_phone(phone)
    
    if not success:
        handle_service_error("хранилища", "обновлении записи", phone)
    
    if not address:
        handle_not_found_error("Запись с указанным номером телефона", phone, "обновления")

    if phone != data.phone:
        logger.info(f"Изменение номера телефона с {phone} на {data.phone}")
        delete_success = await storage_service.delete_phone_address(phone)
        if not delete_success:
            handle_update_error("старой записи", phone, "удалении")

    success = await storage_service.save_phone_address(data.phone, data.address)
    if not success:
        handle_update_error("новых данных", data.phone, "сохранении")
    
    logger.info(f"Запись для телефона {data.phone} успешно обновлена")
    return {"status": "success", "message": "Запись успешно обновлена"}

@router.patch("/{phone}", response_model=SuccessResponse, summary="Частичное обновление адреса")
async def partial_update_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    data: PhoneAddressUpdateData = None,
    storage_service: StorageInterface = Depends(get_storage_service)
):
    logger.info(f"Запрос на частичное обновление адреса для телефона: {phone}")
    address, success = await storage_service.get_address_by_phone(phone)
    
    if not success:
        handle_service_error("хранилища", "частичном обновлении адреса", phone)
    
    if not address:
        handle_not_found_error("Запись с указанным номером телефона", phone, "частичного обновления")
    
    success = await storage_service.save_phone_address(phone, data.address)
    if not success:
        handle_update_error("нового адреса", phone, "сохранении")
    
    logger.info(f"Адрес для телефона {phone} успешно обновлен")
    return {"status": "success", "message": "Адрес успешно обновлен"}

@router.delete("/{phone}", response_model=SuccessResponse, summary="Удаление записи")
async def delete_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    storage_service: StorageInterface = Depends(get_storage_service)
):
    logger.info(f"Запрос на удаление записи для телефона: {phone}")
    address, success = await storage_service.get_address_by_phone(phone)
    
    if not success:
        handle_service_error("хранилища", "удалении записи", phone)
    
    if not address:
        handle_not_found_error("Запись с указанным номером телефона", phone, "удаления")
    
    success = await storage_service.delete_phone_address(phone)
    if not success:
        handle_update_error("записи", phone, "удалении")
    
    logger.info(f"Запись для телефона {phone} успешно удалена")
    return {"status": "success", "message": "Запись успешно удалена"}