from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList
from .pagination import Pagination


def create_response(data, message, status_code):
    result = {
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return Response(result, status=status_code)


def get_first_error_message_from_serializer_errors(serialized_errors, default_message=""):
    if not serialized_errors:
        return default_message
    try:

        serialized_error_dict = serialized_errors
        print(serialized_error_dict)

        if isinstance(serialized_errors, ReturnList):
            serialized_error_dict = serialized_errors[0]

        serialized_errors_keys = list(serialized_error_dict.keys())
        try:
            message = serialized_error_dict[serialized_errors_keys[0]][0].replace("This", serialized_errors_keys[0])
            return message
        except:
            return serialized_error_dict[serialized_errors_keys[0]][0]

    except Exception as e:
        return default_message


def paginate_data(data, request):
    limit = request.query_params.get('limit', None)
    offset = request.query_params.get('offset', None)
    if limit and offset:
        pagination = Pagination()
        data, count = pagination.paginate_queryset(data, request)
        return data, count
    else:
        return data, data.count()