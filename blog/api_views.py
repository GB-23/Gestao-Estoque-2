from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import User, Product, EditedItem, QuickToken
from .serializers import (
    UserSerializer, UserCreateSerializer, UserLoginSerializer,
    ProductSerializer, EditedItemSerializer, QuickTokenSerializer
)
from .utils import generate_code


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():

            if User.objects.filter(email=request.data.get('email')).exists():
                return Response(
                    {"erro": "Email já cadastrado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if request.data.get('cpf') and User.objects.filter(cpf=request.data.get('cpf')).exists():
                return Response(
                    {"erro": "CPF já cadastrado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.save()
            return Response({
                "status": "ok",
                "mensagem": "Usuário cadastrado",
                "id": user.id,
                "nome": user.nome
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            senha = serializer.validated_data['senha']
            
            try:
                user = User.objects.get(email=email)
                if user.senha == senha:
                    return Response({
                        "status": "ok",
                        "mensagem": "Login autorizado",
                        "id": user.id,
                        "nome": user.nome
                    })
                else:
                    return Response(
                        {"erro": "Credenciais inválidas"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except User.DoesNotExist:
                return Response(
                    {"erro": "Credenciais inválidas"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def token_rapido(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"erro": "Usuário não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        codigo = generate_code(7)
        

        QuickToken.objects.filter(email=email).delete()
        
        token = QuickToken.objects.create(
            nome=user.nome,
            email=email,
            codigo=codigo,
            expira_em=timezone.now() + timedelta(hours=1)
        )
        
        return Response({
            "status": "ok",
            "codigo": token.codigo,
            "expira_em": token.expira_em
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class EditedItemViewSet(viewsets.ModelViewSet):
    queryset = EditedItem.objects.all()
    serializer_class = EditedItemSerializer


class QuickTokenViewSet(viewsets.ModelViewSet):
    queryset = QuickToken.objects.all()
    serializer_class = QuickTokenSerializer
