from rest_framework import serializers
from .models import User, Product, EditedItem, QuickToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'idade', 'funcao', 'cpf', 'data_cadastro']
        read_only_fields = ['id', 'data_cadastro']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nome', 'email', 'senha', 'idade', 'funcao', 'cpf']

    def create(self, validated_data):
        user = User.objects.create(
            nome=validated_data['nome'],
            email=validated_data['email'],
            senha=validated_data['senha'],
            idade=validated_data.get('idade'),
            funcao=validated_data.get('funcao'),
            cpf=validated_data.get('cpf')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'nome', 'data_criacao', 'id_informacoes', 'token_produto', 'preco', 'volume', 'validade']
        read_only_fields = ['id', 'data_criacao']


class EditedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditedItem
        fields = ['id', 'data_edicao', 'id_informacoes', 'token_item', 'informacoes_editadas']
        read_only_fields = ['id', 'data_edicao']


class QuickTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickToken
        fields = ['id', 'nome', 'email', 'codigo', 'criado_em', 'expira_em']
        read_only_fields = ['id', 'codigo', 'criado_em']
