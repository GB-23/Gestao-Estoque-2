from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import List_Product, login_view, register_view, logout_view, editar_produto, criar_produto
from .api_views import UserViewSet, ProductViewSet, EditedItemViewSet, QuickTokenViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'edited-items', EditedItemViewSet, basename='edited-item')
router.register(r'quick-tokens', QuickTokenViewSet, basename='quick-token')

urlpatterns = [
    # Autenticação
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Views Django (páginas HTML)
    path('', views.home, name='Home'),
    path('ListProduct/', List_Product, name='ListOgject'),
    path('produto/novo/', criar_produto, name='criar_produto'),
    path('produto/<str:nome>/', views.exibir_produto, name='ListObject'),
    path('produto/<str:nome>/editar/', editar_produto, name='editar_produto'),
    
    # API REST
    path('api/', include(router.urls)),
]
