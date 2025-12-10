from django.contrib import admin
from .models import User, Product, EditedItem, QuickToken, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo')
    list_filter = ('cargo',)
    search_fields = ('user__username', 'user__email')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'funcao', 'data_cadastro')
    list_filter = ('data_cadastro', 'funcao')
    search_fields = ('nome', 'email', 'cpf')
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'idade', 'cpf')
        }),
        ('Segurança', {
            'fields': ('senha',)
        }),
        ('Trabalho', {
            'fields': ('funcao',)
        }),
        ('Datas', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'preco', 'data_criacao', 'data_atualizacao')
    list_filter = ('data_criacao', 'data_atualizacao', 'volume')
    search_fields = ('nome', 'id_informacoes')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'quantidade', 'preco')
        }),
        ('Detalhes do Produto', {
            'fields': ('volume', 'validade', 'imagem')
        }),
        ('Sistema', {
            'fields': ('id_informacoes', 'token_produto'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EditedItem)
class EditedItemAdmin(admin.ModelAdmin):
    list_display = ('token_item', 'produto', 'data_edicao')
    list_filter = ('data_edicao', 'produto')
    search_fields = ('token_item', 'id_informacoes')
    readonly_fields = ('data_edicao',)


@admin.register(QuickToken)
class QuickTokenAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'email', 'ativo', 'criado_em', 'expira_em')
    list_filter = ('ativo', 'criado_em', 'expira_em')
    search_fields = ('codigo', 'email', 'nome')
    readonly_fields = ('criado_em', 'codigo')
    fieldsets = (
        ('Token', {
            'fields': ('codigo', 'email', 'nome', 'usuario')
        }),
        ('Validade', {
            'fields': ('criado_em', 'expira_em', 'ativo')
        }),
    )
