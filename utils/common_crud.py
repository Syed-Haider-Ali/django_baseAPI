from rest_framework.viewsets import ModelViewSet
from utils.helper import create_response, get_first_error_message_from_serializer_errors, paginate_data
from utils.response_messages import *
from django.db.models import Q


class BaseAPIView(ModelViewSet):
    serializer_class = None
    select_related_args = []
    prefetch_related_args = []
    OR_filters = {}
    AND_filters = {}
    order_by = "-id"

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

    def get_records(self, request):
        try:
            order = request.query_params.get('order', 'desc')
            order_by = request.query_params.get('order_by', 'id')
            if order and order_by:
                order_by_ = order_by.lower()
                if hasattr(self.serializer_class.Meta.model, order_by_) and order_by != "id":
                    self.order_by = order_by_
                if order:
                    if order == 'desc':
                        self.order_by = f"-{order_by_}"
                    else:
                        self.order_by = order_by_

            data = self.serializer_class.Meta.model.objects.select_related(*self.select_related_args).prefetch_related(*self.prefetch_related_args).filter(Q(**self.OR_filters, _connector=Q.OR)).filter(**self.AND_filters).order_by(self.order_by)

            data, count = paginate_data(data, request)
            serialized_data = self.serializer_class(data, many=True).data
            response_data = {
                "count": count,
                "data": serialized_data
            }
            return create_response(response_data, SUCCESSFUL, 200)
        except Exception as e:
            return create_response({'error': str(e)}, UNSUCCESSFUL, 500)
