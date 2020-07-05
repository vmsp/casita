from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    distrito = models.TextField()
    concelho = models.TextField()
    freguesia = models.TextField(null=True)

    class Meta:
        db_table = 'locations'

    def __str__(self):
        return f'{self.freguesia}, {self.concelho}, {self.distrito}'


class Ad(models.Model):
    class Source(models.TextChoices):
        OLX = 'OLX', 'OLX'
        IMOVIRTUAL = 'IMOVIRTUAL', 'Imovirtual'
        CUSTO_JUSTO = 'CUSTO_JUSTO', 'Custo Justo'

    class Tipologia(models.TextChoices):
        APARTAMENTO = 'APARTAMENTO', _('Apartamento')
        MORADIA = 'MORADIA', _('Moradia')

    source = models.TextField(choices=Source.choices)
    url = models.URLField(unique=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    for_sale = models.BooleanField()
    cover_photo = models.ImageField(upload_to='thumbs/small/')
    tipologia = models.TextField(choices=Tipologia.choices)
    bedrooms = models.PositiveIntegerField(null=True)
    bathrooms = models.PositiveIntegerField(null=True)
    posted_at = models.DateField()

    # Inutilizados, por agora.
    title = models.TextField()
    description = models.TextField()

    # Estes campos referem-se à inserção/modificação na base de dados.
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'ads'
