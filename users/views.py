from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    operation_description="Получение корневой страницы API со списком доступных эндпоинтов",
    operation_summary="Корневой эндпоинт API",
    tags=["API"],
)
@api_view(["GET"])
def api_root(request):
    """
    Корневой эндпоинт API LMS платформы.
    Возвращает список доступных эндпоинтов системы.
    """
    return Response(
        {
            "message": "Добро пожаловать в LMS API!",
            "endpoints": {
                "courses": "/api/materials/courses/",
                "lessons_list": "/api/materials/lessons/",
                "lesson_create": "/api/materials/lessons/create/",
                "admin": "/admin/",
                "api_auth": "/api-auth/",
                "swagger_docs": "/swagger/",
                "redoc_docs": "/redoc/",
            },
        }
    )
