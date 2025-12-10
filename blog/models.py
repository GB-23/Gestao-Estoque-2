from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser


class UserProfile(models.Model):
    """Perfil estendido do usuário Django"""
    CARGO_CHOICES = [
        ('usuario', 'Usuário'),
        ('gerente', 'Gerente'),
    ]
    
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, related_name='profile')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='usuario', verbose_name='Cargo')
    
    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_cargo_display()}"
    
    def is_gerente(self):
        return self.cargo == 'gerente'


class User(models.Model):
    """Modelo de usuário do sistema"""
    nome = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(unique=True, verbose_name='Email')
    senha = models.CharField(max_length=255, verbose_name='Senha')
    idade = models.IntegerField(null=True, blank=True, verbose_name='Idade')
    funcao = models.CharField(max_length=255, null=True, blank=True, verbose_name='Função')
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name='CPF')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.nome} ({self.email})"


class Product(models.Model):
    """Modelo de produto do inventário"""
    nome = models.CharField(max_length=255, verbose_name='Nome do Produto')
    quantidade = models.IntegerField(default=0, verbose_name='Quantidade em Estoque')
    imagem = models.URLField(max_length=500, null=True, blank=True, verbose_name='URL da Imagem')
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Preço')
    volume = models.CharField(max_length=100, null=True, blank=True, verbose_name='Volume/Tamanho')
    validade = models.DateField(null=True, blank=True, verbose_name='Data de Validade')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    id_informacoes = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID de Informações')
    token_produto = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name='Token do Produto')

    class Meta:
        db_table = 'products'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.quantidade} un)"


class EditedItem(models.Model):
    """Modelo para rastreamento de edições"""
    produto = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Produto')
    data_edicao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Edição')
    id_informacoes = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID de Informações')
    token_item = models.CharField(max_length=255, verbose_name='Token do Item')
    informacoes_editadas = models.TextField(null=True, blank=True, verbose_name='Informações Editadas')

    class Meta:
        db_table = 'edited_items'
        verbose_name = 'Item Editado'
        verbose_name_plural = 'Itens Editados'
        ordering = ['-data_edicao']

    def __str__(self):
        return f"Edição de {self.token_item} em {self.data_edicao.strftime('%d/%m/%Y %H:%M')}"


class QuickToken(models.Model):
    """Modelo para tokens de acesso rápido"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Usuário')
    nome = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    codigo = models.CharField(max_length=10, unique=True, verbose_name='Código')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    expira_em = models.DateTimeField(verbose_name='Expira em')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        db_table = 'quick_tokens'
        verbose_name = 'Token Rápido'
        verbose_name_plural = 'Tokens Rápidos'
        ordering = ['-criado_em']

    def __str__(self):
        return f"Token {self.codigo} - {self.email}"

    def is_valid(self):
        """Verifica se o token ainda é válido"""
        return self.ativo and timezone.now() < self.expira_em

