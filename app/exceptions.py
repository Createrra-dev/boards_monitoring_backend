class BoardMonitoringException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BoardMonitoringException):
    detail = "Объект не найден"
    
    
class ObjectAlreadyexistsException(BoardMonitoringException):
    detail = "Объект уже существует"


class DecodeTokenException(BoardMonitoringException):
    detail = "Ошибка декодирования токена"


class TokenKeysException(BoardMonitoringException):
    detail = "Несоответствие данных токена"


class TokenTypeException(BoardMonitoringException):
    detail = "Не верный тип токена"
    
    
class UserNotFoundException(BoardMonitoringException):
    detail = "Пользователь не найден"
    
    
class VerifyPasswordException(BoardMonitoringException):
    detail = "Пароль введен не верно"