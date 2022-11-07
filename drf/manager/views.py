from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Profile, Transaction
from .serializer import (CategorySerializer, RegisterSerializer,
                         TransactionSerializer, UserSerializer)

# Create your views here.

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.filter(id=self.request.user.id)
        return queryset


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Profile.objects.get(id=self.request.user.id).categories
        return queryset


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user.id)
        return queryset

    def get_permissions(self):
        SAVE = ['list', 'create', 'filter_transaction']
        if self.action in SAVE:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['GET'], detail=False)
    def filter_transaction(self, request, *args, **kwargs):
        ordering = request.GET.get('ordering')
        queryset = self.get_queryset().values()
        if ordering:
            queryset = queryset.order_by(ordering)
        return Response(queryset)
