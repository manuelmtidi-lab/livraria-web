from django.shortcuts import render, get_object_or_404
from .models import Livro


def catalogo(request):
    from django.db.models import Q
    q = request.GET.get('q', '').strip()
    livros = Livro.objects.select_related('autor', 'editora').order_by('titulo')
    if q:
        livros = livros.filter(Q(titulo__icontains=q) | Q(autor__nome__icontains=q) | Q(editora__nome__icontains=q))
    return render(request, 'livraria/catalogo.html', {'livros': livros, 'q': q})


def detalhe_livro(request, livro_id):
    livro = get_object_or_404(Livro, id=livro_id)
    return render(request, 'livraria/detalhe.html', {'livro': livro})


from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import CadastroForm


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('catalogo')
    else:
        form = CadastroForm()
    return render(request, 'livraria/cadastro.html', {'form': form})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from .models import Cliente, Venda


@login_required
def comprar(request, livro_id):
    if request.method != 'POST':
        return redirect('detalhe_livro', livro_id=livro_id)

    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, 'Esta conta não é de cliente. Entre com uma conta criada pelo cadastro.')
        return redirect('detalhe_livro', livro_id=livro_id)

    try:
        quantidade = int(request.POST.get('quantidade', 1))
    except ValueError:
        quantidade = 0
    if quantidade < 1:
        messages.error(request, 'Quantidade inválida.')
        return redirect('detalhe_livro', livro_id=livro_id)

    with transaction.atomic():
        livro = Livro.objects.select_for_update().get(id=livro_id)
        if quantidade > livro.quantidade:
            messages.error(request, f'Stock insuficiente. Disponível: {livro.quantidade}.')
            return redirect('detalhe_livro', livro_id=livro_id)

        venda = Venda.objects.create(
            cliente=cliente,
            livro=livro,
            quantidade=quantidade,
            preco_venda=livro.preco_venda,
            data_venda=timezone.localdate(),
        )
        livro.quantidade -= quantidade
        livro.save()

    return redirect('confirmacao', venda_id=venda.id)


@login_required
def confirmacao(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id, cliente__usuario=request.user)
    total = venda.preco_venda * venda.quantidade
    return render(request, 'livraria/confirmacao.html', {'venda': venda, 'total': total})


@login_required
def minhas_compras(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.error(request, 'Esta conta não é de cliente.')
        return redirect('catalogo')

    vendas = (Venda.objects
              .filter(cliente=cliente)
              .select_related('livro')
              .order_by('-data_venda', '-id'))

    for v in vendas:
        v.total = v.preco_venda * v.quantidade

    total_gasto = sum(v.total for v in vendas)
    return render(request, 'livraria/minhas_compras.html',
                  {'vendas': vendas, 'total_gasto': total_gasto})
