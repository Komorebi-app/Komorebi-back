from rest_framework import status
from rest_framework.response import Response

class JsonResponse:

    @staticmethod
    def success(data):
        return Response(data, status=status.HTTP_200_OK)

    @staticmethod
    def response(data: dict | list, code: int):
        return Response(data, status=code)

    @staticmethod
    def paginated(count: int, next_page: int|None, previous_page: int|None, results: list):
        return JsonResponse.success({
            "count": count,
            "next": next_page,
            "previous": previous_page,
            "results": results
        })

    @staticmethod
    def not_implemented():
        return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
