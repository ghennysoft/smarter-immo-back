from cours.models import Cour
from cours.serializers import CourSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated


class CourView(generics.ListAPIView):
    queryset = Cour.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CourSerializer

class CourDetail(generics.RetrieveAPIView):
    queryset = Cour.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CourSerializer