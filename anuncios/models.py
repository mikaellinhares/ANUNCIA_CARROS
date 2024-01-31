from django.db import models
from vendedores.models import Vendedor


class TipoVeiculo(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.nome


class OpcionalVeiculo(models.Model):
    nome = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.nome


class CorVeiculo(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.nome


class MarcaVeiculo(models.Model):
    nome = models.CharField(max_length=200)
    modelos = models.ManyToManyField('ModeloVeiculo', related_name='modelos', blank=True)

    def __str__(self) -> str:
        return self.nome


class ModeloVeiculo(models.Model):
    nome = models.CharField(max_length=200)
    marca = models.ForeignKey('MarcaVeiculo', on_delete=models.CASCADE)
    tipo = models.ForeignKey('TipoVeiculo', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.nome


class ImagemAnuncio(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='anuncios')
    anuncio = models.ForeignKey('Anuncio', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome


class Anuncio(models.Model):
    descricao = models.TextField(max_length=1500)

    ano = models.PositiveIntegerField()
    valor = models.PositiveIntegerField()
    quilometragem = models.PositiveIntegerField()

    cor = models.ForeignKey(CorVeiculo, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(MarcaVeiculo, on_delete=models.SET_NULL, null=True)
    modelo = models.ForeignKey(ModeloVeiculo, on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

    imagens = models.ManyToManyField(ImagemAnuncio, related_name='imagens', blank=True)
    opcionais = models.ManyToManyField(OpcionalVeiculo, blank=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} {self.ano}'

    def valor_formatado(self):
        return f'R$ {self.valor:_.2f}'.replace('.', ',').replace('_', '.')

    def km_formatado(self):
        return f'{self.quilometragem:_.0f} Km'.replace('_', '.')
