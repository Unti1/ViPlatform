import enum

class GenderEnum(str, enum.Enum):
    UNDEFINE = 'Не определено'
    MALE = 'Мужчина'
    FEMALE = 'Женщина'
    
class StatusEnum(str, enum.Enum):
    DEMO = 'Демонстрационный'
    BASE = 'Обычный'
    PRO = 'Расширенный'
    ADMIN = 'Администраторский'
    CREATOR = 'Создатель'

class RoleEnum(str, enum.Enum):
    TEACHER = 'Учитель'
    STUDENT = 'Ученик'