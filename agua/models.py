from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _

class YearMonthField(forms.DateField):
    default_error_messages = {
        'invalid': _("Please specify a valid year month.")
    }
    widget = forms.DateInput(format='%m/%Y')
    input_formats = ('%m/%Y', '%m/%y')

    def to_python(self, value):
        """
        Set day to first day of month.
        """
        value = super(YearMonthField, self).to_python(value)
        return datetime.date(value.year, value.month, 1)

class Competencia(models.Model):
    ABERTO='AB'
    FECHADO='FC'
    COMPETENCIA_STATUS_CHOICES = (
        ( ABERTO , _('Open')),
        ( FECHADO, _('Closed')),
    )
    competencia = models.DateField()   # 01/Mes/Ano da Competencia
    data_fechamento = models.DateField(null=True,blank=True)  # Data do fechamento da Competencia
    situacao = models.CharField(max_length=2,choices=COMPETENCIA_STATUS_CHOICES,default=ABERTO)

    def __str__(self):
        return str(self.competencia.strftime('%m/%Y'))

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
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return "%s [%s]" % (self.nome_conhecido , self.nome_completo)

    def get_absolute_url(self):
        return reverse('condomino_edit',kwargs={'pk': self.pk})


class CondominoDoCondominio(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    condomino = models.ForeignKey(Condomino, on_delete=models.CASCADE)
    data_inicio = models.DateField(blank=True)

    def __str__(self):
        return "%s [%s]" % (self.condomino.nome_conhecido , self.condominio.nome)

    def get_absolute_url(self):
        return reverse('condomino_do_condominio_edit',kwargs={'pk': self.pk})


class Hidrometro(models.Model):
    condominoDoCondominio = models.ForeignKey(CondominoDoCondominio, on_delete=models.CASCADE)
    identificacao = models.CharField(max_length=100)
    casasDecimais = models.IntegerField()

    @property
    def ultima_medicao(self):
        print("ultima")
        print(self.id)
        return Medicao.objects.filter(hidrometro=self.id).latest('data_medicao')

    def __str__(self):
        return "%s [%s]" % (self.condominoDoCondominio.condomino.nome_conhecido , self.identificacao)


    def get_absolute_url(self):
        return reverse('hidrometro_edit',kwargs={'pk': self.pk})


class Medicao(models.Model):
    hidrometro = models.ForeignKey(Hidrometro, on_delete=models.CASCADE)
    data_medicao = models.DateField()
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT,null=True)
    medicao = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return "%s / %s - %s" % (self.hidrometro  , self.data_medicao , self.medicao )


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
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT, null=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.tipo_despesa.descricao + " [" + str(self.data_despesa) + "] " + str(self.cmpt) + " "+ str(self.valor)

    def get_absolute_url(self):
        return reverse('despesa_edit',kwargs={'pk': self.pk})

class PagamentoCondomino(models.Model):
    condominoDoCondominio = models.ForeignKey(CondominoDoCondominio, on_delete=models.SET_NULL, null=True)
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT, null=True)
    data_pagamento = models.DateField(null=True,blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=18, decimal_places=2)
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super(Agua, self).save(*args,**kwargs)
