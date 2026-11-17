from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F


class Autor(models.Model):
    nome = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Autores"

    def __str__(self):
        return self.nome


class Editora(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    nome = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT)
    edicao_volume = models.CharField(max_length=50, blank=True)
    data_publicacao = models.DateField(null=True, blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField(default=0)
    capa = models.ImageField(upload_to='capas/', null=True, blank=True)

    @property
    def cor_capa(self):
        return (self.id or 0) % 6

    @property
    def paleta(self):
        return [
            'bg-tijolo text-[#f7e6d3]',
            'bg-floresta text-[#ecdfc4]',
            'bg-ouro text-[#2a1f10]',
            'bg-[#2d3e5a] text-[#efe3cc]',
            'bg-[#d9c3a0] text-[#3a1f17]',
            'bg-[#4a2a3a] text-[#f1dccb]',
        ][self.cor_capa]

    def __str__(self):
        return self.titulo


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente}"


class Compra(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2)
    data_compra = models.DateField()

    def save(self, *args, **kwargs):
        # So aumenta o stock quando a compra e nova
        e_nova = self.pk is None
        with transaction.atomic():
            super().save(*args, **kwargs)
            if e_nova:
                Livro.objects.filter(pk=self.livro_id).update(
                    quantidade=F('quantidade') + self.quantidade
                )

    def __str__(self):
        return f"Compra #{self.id} - {self.fornecedor}"
