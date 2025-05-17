from fastapi import APIRouter, HTTPException, Depends, Path, status
from app.models.models import PhoneAddressData,SuccessResponse, PhoneAddressUpdateData
from app.services.services import RedisService
from app.utils.logging import logger

router = APIRouter(prefix="/contacts", tags=["Contacts"])

def get_redis_service():
    return RedisService()

@router.get("/{phone}", response_model=dict, summary="Получение адреса по номеру телефона")
async def get_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    redis_service: RedisService = Depends(get_redis_service)
):
    logger.info(f"Запрос адреса для телефона: {phone}")
    address, success = await redis_service.get_address_by_phone(phone)
    
    if not success:
        logger.error(f"Ошибка сервиса при получении адреса для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Сервис временно недоступен"
        )
    
    if not address:
        logger.info(f"Адрес для телефона {phone} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Адрес не найден"
        )
    
    logger.info(f"Адрес для телефона {phone} успешно получен")
    return {"phone": phone, "address": address}

@router.post("/", response_model=SuccessResponse, summary="Создание новой записи")
async def create_phone_address(
    data: PhoneAddressData,
    redis_service: RedisService = Depends(get_redis_service)
):
    logger.info(f"Запрос на создание записи для телефона: {data.phone}")
    
    existing_address, success = await redis_service.get_address_by_phone(data.phone)
    
    if not success:
        logger.error(f"Ошибка сервиса при проверке существования телефона: {data.phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Сервис временно недоступен"
        )
    
    if existing_address:
        logger.warning(f"Попытка создать запись для существующего телефона: {data.phone}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Запись с указанным номером телефона уже существует"
        )
    
    success = await redis_service.save_phone_address(data.phone, data.address)
    if not success:
        logger.error(f"Ошибка при сохранении данных для телефона: {data.phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ошибка при сохранении данных"
        )
    
    logger.info(f"Запись для телефона {data.phone} успешно создана")
    return {"status": "success", "message": "Данные успешно сохранены"}

@router.put("/{phone}", response_model=SuccessResponse, summary="Полное обновление записи")
async def update_phone_address(
    phone: str = Path(..., description="Текущий номер телефона в формате 8XXXXXXXXXX"),
    data: PhoneAddressData = None,
    redis_service: RedisService = Depends(get_redis_service)
):
    logger.info(f"Запрос на обновление записи для телефона: {phone}")
    address, success = await redis_service.get_address_by_phone(phone)
    
    if not success:
        logger.error(f"Ошибка сервиса при обновлении записи для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Сервис временно недоступен"
        )
    
    if not address:
        logger.info(f"Запись для телефона {phone} не найдена при попытке обновления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Запись с указанным номером телефона не найдена"
        )

    if phone != data.phone:
        logger.info(f"Изменение номера телефона с {phone} на {data.phone}")
        delete_success = await redis_service.delete_phone_address(phone)
        if not delete_success:
            logger.error(f"Ошибка при удалении старой записи для телефона: {phone}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="Ошибка при обновлении данных"
            )

    success = await redis_service.save_phone_address(data.phone, data.address)
    if not success:
        logger.error(f"Ошибка при сохранении новых данных для телефона: {data.phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ошибка при обновлении данных"
        )
    
    logger.info(f"Запись для телефона {data.phone} успешно обновлена")
    return {"status": "success", "message": "Запись успешно обновлена"}

@router.patch("/{phone}", response_model=SuccessResponse, summary="Частичное обновление адреса")
async def partial_update_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    data: PhoneAddressUpdateData = None,
    redis_service: RedisService = Depends(get_redis_service)
):
    logger.info(f"Запрос на частичное обновление адреса для телефона: {phone}")
    address, success = await redis_service.get_address_by_phone(phone)
    
    if not success:
        logger.error(f"Ошибка сервиса при частичном обновлении адреса для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Сервис временно недоступен"
        )
    
    if not address:
        logger.info(f"Запись для телефона {phone} не найдена при попытке частичного обновления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Запись с указанным номером телефона не найдена"
        )
    
    success = await redis_service.save_phone_address(phone, data.address)
    if not success:
        logger.error(f"Ошибка при сохранении нового адреса для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ошибка при обновлении данных"
        )
    
    logger.info(f"Адрес для телефона {phone} успешно обновлен")
    return {"status": "success", "message": "Адрес успешно обновлен"}

@router.delete("/{phone}", response_model=SuccessResponse, summary="Удаление записи")
async def delete_phone_address(
    phone: str = Path(..., description="Номер телефона в формате 8XXXXXXXXXX"),
    redis_service: RedisService = Depends(get_redis_service)
):
    logger.info(f"Запрос на удаление записи для телефона: {phone}")
    address, success = await redis_service.get_address_by_phone(phone)
    
    if not success:
        logger.error(f"Ошибка сервиса при удалении записи для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Сервис временно недоступен"
        )
    
    if not address:
        logger.info(f"Запись для телефона {phone} не найдена при попытке удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Запись с указанным номером телефона не найдена"
        )
    
    success = await redis_service.delete_phone_address(phone)
    if not success:
        logger.error(f"Ошибка при удалении записи для телефона: {phone}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Ошибка при удалении данных"
        )
    
    logger.info(f"Запись для телефона {phone} успешно удалена")
    return {"status": "success", "message": "Запись успешно удалена"}
