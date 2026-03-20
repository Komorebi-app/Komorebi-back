from typing import Any, Dict, Optional

from rest_framework import status

from logs.logger import logger
from logs.models import Log
from logs.levels import LogLevel

from core.utils.response import JsonResponse
from core.utils.validation import ValidationErrorItem

class Logger():

    def __init__(self, log):
        self.log = log

    def validationErrors(self, username: str, errors: list[ValidationErrorItem]):
        return self.new(
            level = LogLevel.ERROR,
            message = "Import failed",
            context = {
                "count": len(errors),
                "errors": errors,
                "user": username
            },
            http_code = status.HTTP_400_BAD_REQUEST
        )

    def invalid_fields(self, fileds: dict):
        return self.new(
            level = LogLevel.ERROR,
            message = f"Invalid relational field{'s' if len(fileds) > 1 else ''}",
            context = {
                "fields": fileds
            },
            http_code = status.HTTP_400_BAD_REQUEST
        )

    def new(
        self,
        level: LogLevel = LogLevel.INFO,
        message: str = "",
        context: Optional[Dict[str, Any]] = None,
        http_code: int = status.HTTP_200_OK
    ):
        Log.objects.create(
            type = level,
            message = message,
            context = context
        )
        return JsonResponse.response({
            "level": level,
            "message": message,
            "context": context
        }, http_code)

logger = Logger(logger)
