from typing import Any, Optional

from fastapi.responses import JSONResponse


class Success(JSONResponse):
    def __init__(
        self,
        code: int = 200,
        message: Optional[str] = "OK",
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "message": message, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)


class Fail(JSONResponse):
    def __init__(
        self,
        code: int = 400,
        msg: Optional[str] = None,
        data: Optional[Any] = None,
        **kwargs,
    ):
        content = {"code": code, "msg": msg, "data": data}
        content.update(kwargs)
        super().__init__(content=content, status_code=code)
