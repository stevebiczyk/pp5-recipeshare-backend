from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response


@require_GET
@never_cache
@ensure_csrf_cookie
def csrf_route(request):
    # Return the masked token so an allowed frontend on another host can use it.
    return JsonResponse({"csrfToken": get_token(request)})


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my PP5 API!"
    })

# # dj-rest-auth logout view fix
# @api_view(['POST'])
# def logout_route(request):
#     response = Response()
#     response.set_cookie(
#         key=JWT_AUTH_COOKIE,
#         value='',
#         httponly=True,
#         expires='Thu, 01 Jan 1970 00:00:00 GMT',
#         max_age=0,
#         samesite=JWT_AUTH_SAMESITE,
#         secure=JWT_AUTH_SECURE,
#     )
#     response.set_cookie(
#         key=JWT_AUTH_REFRESH_COOKIE,
#         value='',
#         httponly=True,
#         expires='Thu, 01 Jan 1970 00:00:00 GMT',
#         max_age=0,
#         samesite=JWT_AUTH_SAMESITE,
#         secure=JWT_AUTH_SECURE,
#     )
#     return response
