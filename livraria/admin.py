from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Autor, Cliente, Compra, Editora, Fornecedor, Livro, Venda

# ---- Utilizadores e grupos com o novo visual ----
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


# ---- Tabelas simples ----
@admin.register(Autor)
class AutorAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Editora)
class EditoraAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Fornecedor)
class FornecedorAdmin(ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ('nome', 'usuario')
    search_fields = ('nome', 'usuario__username')


# ---- Livros ----
@admin.register(Livro)
class LivroAdmin(ModelAdmin):
    list_display = ('titulo', 'autor', 'editora', 'preco_venda', 'estado_stock')
    list_filter = ('autor', 'editora')
    search_fields = ('titulo', 'autor__nome', 'editora__nome')
    autocomplete_fields = ('autor', 'editora')
    list_per_page = 20

    @display(description="Stock", label={"Esgotado": "danger", "Pouco": "warning", "OK": "success"})
    def estado_stock(self, obj):
        if obj.quantidade == 0:
            return "Esgotado", f"{obj.quantidade} un."
        if obj.quantidade <= 3:
            return "Pouco", f"{obj.quantidade} un."
        return "OK", f"{obj.quantidade} un."


# ---- Vendas ----
@admin.register(Venda)
class VendaAdmin(ModelAdmin):
    list_display = ('id', 'cliente', 'livro', 'quantidade', 'preco_venda', 'total', 'data_venda')
    list_filter = ('data_venda',)
    search_fields = ('cliente__nome', 'livro__titulo')
    autocomplete_fields = ('cliente', 'livro')
    date_hierarchy = 'data_venda'

    @display(description="Total")
    def total(self, obj):
        return f"{obj.preco_venda * obj.quantidade} Kz"


# ---- Compras a fornecedores ----
@admin.register(Compra)
class CompraAdmin(ModelAdmin):
    list_display = ('id', 'fornecedor', 'livro', 'quantidade', 'preco_compra', 'total', 'data_compra')
    list_filter = ('data_compra', 'fornecedor')
    search_fields = ('fornecedor__nome', 'livro__titulo')
    autocomplete_fields = ('fornecedor', 'livro')
    date_hierarchy = 'data_compra'

    @display(description="Total")
    def total(self, obj):
        return f"{obj.preco_compra * obj.quantidade} Kz"
