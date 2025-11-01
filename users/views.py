from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'Добро пожаловать в LMS API!',
        'endpoints': {
            'courses': '/api/materials/courses/',
            'lessons_list': '/api/materials/lessons/',
            'lesson_create': '/api/materials/lessons/create/',
            'admin': '/admin/',
            'api_auth': '/api-auth/'
        }
    })