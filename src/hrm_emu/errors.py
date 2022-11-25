class HRM_EXCEPTION(BaseException):
    pass

class EMPTY_VALUE(HRM_EXCEPTION):
    pass

class INVALID_OPCODE(HRM_EXCEPTION):
    pass

class TYPE_ERROR(HRM_EXCEPTION):
    pass

class OUT_OF_BOUNDS(HRM_EXCEPTION):
    pass

class OVERFLOW(HRM_EXCEPTION):
    pass