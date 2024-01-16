from rest_framework.viewsets import ModelViewSet
from utils.helper import create_response, get_first_error_message_from_serializer_errors
from utils.response_messages import *


class BaseAPIView(ModelViewSet):
    def create_record(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)
            if serialized_data.is_valid():
                response_data = serialized_data.save()
                return create_response(self.serializer_class(response_data).data, SUCCESSFUL, status_code=200)
            return create_response({},
                                   get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL),
                                   status_code=400)
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(str(e))
                return create_response({}, self.feature_name + " " + ALREADY_EXISTS, 400)
            print(str(e))
            return create_response({str(e)}, UNSUCCESSFUL, 500)