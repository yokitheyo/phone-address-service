from abc import ABC, abstractmethod
from typing import Optional, Tuple

class StorageInterface(ABC):
    @abstractmethod
    async def get_address_by_phone(self, phone: str) -> Tuple[Optional[str], bool]:
        pass
    
    @abstractmethod
    async def save_phone_address(self, phone: str, address: str) -> bool:
        pass
    
    @abstractmethod
    async def delete_phone_address(self, phone: str) -> bool:
        pass
    
    @abstractmethod
    async def ping(self) -> bool:
        pass