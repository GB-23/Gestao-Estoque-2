from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Product, EditedItem, UserProfile


def gerente_required(view_func):
    """Decorator para verificar se o usuário é gerente"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.is_gerente():
                messages.error(request, 'Você não tem permissão para acessar essa funcionalidade. Apenas gerentes podem.')
                return redirect('ListOgject')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Perfil de usuário não encontrado.')
            return redirect('ListOgject')
        
        return view_func(request, *args, **kwargs)
    
    return login_required(login_url='login')(wrapper)


@login_required(login_url='login')
def home(request):
    """Página inicial - Redireciona para lista de produtos se logado"""
    return redirect('ListOgject')


def login_view(request):
    """Página de login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('ListOgject')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'login_page.html')


def register_view(request):
    """Página de cadastro"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validações
        if not all([username, email, first_name, password, password_confirm]):
            messages.error(request, 'Por favor, preencha todos os campos.')
            return redirect('register')
        
        if password != password_confirm:
            messages.error(request, 'As senhas não correspondem.')
            return redirect('register')
        
        if len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nome de usuário já existe.')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este email já está cadastrado.')
            return redirect('register')
        
        # Criar usuário
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name
            )
            UserProfile.objects.create(user=user, cargo='usuario')
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}')
            return redirect('register')
    
    return render(request, 'register_page.html')


def logout_view(request):
    """Fazer logout"""
    logout(request)
    messages.success(request, 'Você foi desconectado.')
    return redirect('login')


@gerente_required
def criar_produto(request):
    """Criar novo produto"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade', 0)
        preco = request.POST.get('preco')
        volume = request.POST.get('volume')
        validade = request.POST.get('validade')
        imagem = request.POST.get('imagem')
        
        if not nome:
            messages.error(request, 'Nome do produto é obrigatório.')
            return redirect('criar_produto')
        
        if Product.objects.filter(nome=nome).exists():
            messages.error(request, 'Já existe um produto com este nome.')
            return redirect('criar_produto')
        
        try:
            produto = Product.objects.create(
                nome=nome,
                quantidade=int(quantidade) if quantidade else 0,
                preco=float(preco) if preco else None,
                volume=volume,
                validade=validade if validade else None,
                imagem=imagem
            )
            
            messages.success(request, f'Produto "{produto.nome}" criado com sucesso!')
            return redirect('ListOgject')
        except Exception as e:
            messages.error(request, f'Erro ao criar produto: {str(e)}')
            return redirect('criar_produto')
    
    return render(request, 'criar_produto.html')


@login_required(login_url='login')
def List_Product(request):
    """Lista produtos do banco de dados com paginação"""
    produtos = Product.objects.all()
    

    try:
        is_gerente = request.user.profile.is_gerente()
    except UserProfile.DoesNotExist:
        is_gerente = False
    

    html_cards = "<tr>"
    for i, produto in enumerate(produtos, start=1):

        url_editar = reverse('editar_produto', kwargs={'nome': produto.nome})
        
        imagem_url = produto.imagem or ''
        
        botao_editar = ""
        if is_gerente:
            botao_editar = f"""<button onclick="window.location.href='{url_editar}'" class="btn-controlar"><i class="fas fa-pencil-alt"></i> EDITAR</button>"""
        
        html_cards += f"""
            <td>
                <div class="card">
                    <img src="{imagem_url}" alt="{produto.nome}" onerror="this.src=''">
                    <h3>{produto.nome}</h3>
                    <p>{produto.quantidade} Und</p>
                    <div class="botoes">
                        {botao_editar}
                    </div>
                </div>
            </td>
        """
        if i % 5 == 0:
            html_cards += "</tr><tr>"
    html_cards += "</tr>"
    
    return render(request, 'list.html', {
        'cards_html': html_cards,
        'total_produtos': produtos.count(),
        'usuario': request.user,
        'is_gerente': is_gerente
    })


@login_required(login_url='login')
def exibir_produto(request, nome):
    """Página de detalhes do produto"""
    try:
        produto = Product.objects.get(nome=nome)
        imagem_url = produto.imagem or ''
        contexto = {
            'numero_produto': produto.nome,
            'objeto_imagem_url': imagem_url,
            'produto': produto,
            'preco': produto.preco,
            'quantidade': produto.quantidade,
            'volume': produto.volume,
            'validade': produto.validade,
        }
    except Product.DoesNotExist:
        contexto = {
            'numero_produto': nome,
            'objeto_imagem_url': '',
            'produto': None,
        }
    
    return render(request, 'produto.html', contexto)


@gerente_required
def editar_produto(request, nome):
    """Página de edição do produto"""
    try:
        produto = Product.objects.get(nome=nome)
    except Product.DoesNotExist:
        messages.error(request, 'Produto não encontrado.')
        return redirect('ListOgject')
    
    if request.method == 'POST':
        # Verificar se é solicitação de exclusão
        if request.POST.get('action') == 'delete':
            try:
                produto_nome = produto.nome
                produto.delete()
                messages.success(request, f'Produto "{produto_nome}" deletado com sucesso!')
                return redirect('ListOgject')
            except Exception as e:
                messages.error(request, f'Erro ao deletar produto: {str(e)}')
                return redirect('ListOgject')
        
        # Caso contrário, atualizar o produto
        produto.quantidade = request.POST.get('quantidade', produto.quantidade)
        produto.preco = request.POST.get('preco', produto.preco)
        produto.volume = request.POST.get('volume', produto.volume)
        produto.validade = request.POST.get('validade', produto.validade)
        produto.imagem = request.POST.get('imagem', produto.imagem)
        
        try:
            produto.full_clean() 
            produto.save()
            
            EditedItem.objects.create(
                produto=produto,
                token_item=f"{produto.nome}_{produto.id}",
                informacoes_editadas=f"Atualizado em {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
            
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('ListOgject')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar produto: {str(e)}')
    
    imagem_url = produto.imagem or ''
    
    contexto = {
        'produto': produto,
        'imagem_url': imagem_url,
    }
    
    return render(request, 'editar_produto.html', contexto)
