from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def check_parameters(*expected_params, methods=('POST', 'PUT', 'PATCH')):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method in methods:
                params_from_request = list(request.data)
                missing_params = [param for param in expected_params if param not in params_from_request]
                if missing_params:
                    return Response({'error': f'Missing parameters: {", ".join(missing_params)}'}, status=status.HTTP_400_BAD_REQUEST)
                return view_func(request, *args, **kwargs)
            else:
                return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return wrapper
    return decorator
