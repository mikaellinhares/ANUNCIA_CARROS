from django.db import models
import phonenumbers


map_estados = [
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins')
]


class Vendedor(models.Model):
    nome = models.CharField(max_length=200)
    contato = models.PositiveIntegerField()
    logo = models.ImageField(upload_to="logos", blank=True, null=True)

    anuncios = models.ManyToManyField('anuncios.Anuncio', related_name='anuncios', blank=True)

    endereco_rua = models.CharField(max_length=100, blank=True, null=True)
    endereco_numero = models.PositiveIntegerField(blank=True, null=True)
    endereco_bairro = models.CharField(max_length=50, blank=True, null=True)
    endereco_cidade = models.CharField(max_length=50, blank=True, null=True)
    endereco_estado = models.CharField(max_length=50, blank=True, null=True, choices=map_estados)

    def __str__(self):
        return self.nome

    def contato_formatado(self):
        contato_ajustado = phonenumbers.parse(str(self.contato), "BR")
        contato_ajustado = phonenumbers.format_number(contato_ajustado, phonenumbers.PhoneNumberFormat.NATIONAL)
        return contato_ajustado
