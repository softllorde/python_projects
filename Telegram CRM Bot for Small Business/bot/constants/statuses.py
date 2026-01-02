from enum import Enum


class ClientStatus(str, Enum):
    NEW = "Новый"
    IN_PROGRESS = "В работе"
    DONE = "Завершён"
