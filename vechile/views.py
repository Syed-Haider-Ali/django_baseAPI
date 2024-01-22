from .serializers import MakeSerializer, VechileSerializer
from utils.common_crud import BaseAPIView

class MakeAPIView(BaseAPIView):
    serializer_class = MakeSerializer


class VechileAPIView(BaseAPIView):
    serializer_class = VechileSerializer
    prefetch_related_args = ['make']
