from rest_framework.viewsets import ModelViewSet
from utils.helper import create_response, get_first_error_message_from_serializer_errors, paginate_data
from utils.response_messages import *


class BaseAPIView(ModelViewSet):
    serializer_class = None
    select_related_args = []
    prefetch_related_args = []

    def create_record(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                return create_response(self.serializer_class(response_data).data, SUCCESSFUL, 200)
            return create_response({},
                                   get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL),
                                   400)
        except Exception as e:
            return create_response({str(e)}, UNSUCCESSFUL, 500)


