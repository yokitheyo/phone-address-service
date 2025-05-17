from fastapi import HTTPException, status
from app.utils.logging import logger

def handle_service_error(service_name: str, operation: str, entity_id: str):
    logger.error(f"Ошибка сервиса при {operation} {service_name} для {entity_id}")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Сервис временно недоступен"
    )

def handle_not_found_error(entity_type: str, entity_id: str, operation: str = None):
    operation_text = f" при попытке {operation}" if operation else ""
    logger.info(f"{entity_type} для {entity_id} не найден{operation_text}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity_type} не найден"
    )

def handle_conflict_error(entity_type: str, entity_id: str):
    logger.warning(f"Попытка создать {entity_type} для существующего {entity_id}")
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{entity_type} с указанным номером телефона уже существует"
    )

def handle_update_error(entity_type: str, entity_id: str, operation: str):
    logger.error(f"Ошибка при {operation} {entity_type} для {entity_id}")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=f"Ошибка при {operation} данных"
    )