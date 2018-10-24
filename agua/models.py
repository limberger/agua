from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

class Condominio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('condominio_edit',kwargs={'pk': self.pk})

class Condomino(models.Model):
    nome_conhecido = models.CharField(max_length=50)
    nome_completo = models.CharField(max_length=150)
    email = models.EmailField(max_length=254,blank=True)

    def __str__(self):
        return "%s [%s]" % (self.nome_conhecido , self.nome_completo)

    def get_absolute_url(self):
        return reverse('condomino_edit',kwargs={'pk': self.pk})


class CondominoDoCondominio(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    condomino = models.ForeignKey(Condomino, on_delete=models.CASCADE)
    data_inicio = models.DateField()

    def __str__(self):
        return "%s [%s]" % (self.condomino.nome_conhecido , self.condominio.nome)

    def get_absolute_url(self):
        return reverse('condomino_do_condominio_edit',kwargs={'pk': self.pk})


class Hidrometro(models.Model):
    condominoDoCondominio = models.ForeignKey(CondominoDoCondominio, on_delete=models.CASCADE)
    identificacao = models.CharField(max_length=100)

    def __str__(self):
        return "%s [%s]" % (self.condominoDoCondominio.condomino.nome_conhecido , self.identificacao)

    def get_absolute_url(self):
        return reverse('hidrometro_edit',kwargs={'pk': self.pk})


class Medicao(models.Model):
    hidrometro = models.ForeignKey(Hidrometro, on_delete=models.CASCADE)
    data_medicao = models.DateField()
    competencia = models.DateField()
    medicao = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return "%s [%s]" % (self.hidrometro.identicacao , self.data_medicao )

    def get_absolute_url(self):
        return reverse('medicao_edit',kwargs={'pk': self.pk})

class TipoDespesa(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.condominio.nome, self.descricao )

    def get_absolute_url(self):
        return reverse('tipo_despesa_edit',kwargs={'pk': self.pk})


class Despesa(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    tipo_despesa = models.ForeignKey(TipoDespesa, on_delete=models.CASCADE)
    data_despesa = models.DateField()
    competencia = models.DateField()
    descricao = models.Charfield(max_length=200)
    valor = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.tipo_despesa.descricao + " [" + self.data_despesa + "]"

    def get_absolute_url(self):
        return reverse('despesa_edit',kwargs={'pk': self.pk})

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super(Agua, self).save(*args,**kwargs)
