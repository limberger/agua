from datetime import datetime

from django.db import models
from django.urls import reverse
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


class Condominio(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('condominio_edit', kwargs={'pk': self.pk})


class Competencia(models.Model):
    ABERTO = 'AB'
    FECHADO = 'FC'
    COMPETENCIA_STATUS_CHOICES = (
        (ABERTO, _('Open')),
        (FECHADO, _('Closed')),
    )
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    competencia = models.DateField()  # 01/Mes/Ano da Competencia
    data_fechamento = models.DateField(null=True, blank=True)  # Data do fechamento da Competencia
    situacao = models.CharField(max_length=2, choices=COMPETENCIA_STATUS_CHOICES, default=ABERTO)

    @property
    def extenso(self):
        mes = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')

        nr_mes = self.competencia.month - 1
        ano = self.competencia.year

        return "%s de %d." % (mes[nr_mes], ano)

    class Meta:
        get_latest_by = 'competencia'

    def __str__(self):
        return str(self.competencia.strftime('%m/%Y'))


class Condomino(models.Model):
    nome_conhecido = models.CharField(max_length=50)
    nome_completo = models.CharField(max_length=150)
    condominio = models.ForeignKey(Condominio, on_delete=models.PROTECT)
    endereco_unidade = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s [%s]" % (self.nome_conhecido, self.nome_completo)

    def get_absolute_url(self):
        return reverse('condomino_edit', kwargs={'pk': self.pk})


class Hidrometro(models.Model):
    condomino = models.ForeignKey(Condomino, on_delete=models.PROTECT)
    identificacao = models.CharField(max_length=100)
    casasDecimais = models.IntegerField()

    @property
    def ultima_medicao(self):
        print("ultima")
        print(self.id)
        return Medicao.objects.filter(hidrometro=self.id).latest('data_medicao')

    def __str__(self):
        return "%s [%s]" % (self.condomino.nome_conhecido, self.identificacao)

    def get_absolute_url(self):
        return reverse('hidrometro_edit', kwargs={'pk': self.pk})


class Medicao(models.Model):
    hidrometro = models.ForeignKey(Hidrometro, on_delete=models.CASCADE)
    data_medicao = models.DateField()
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT, null=True)
    medicao = models.DecimalField(max_digits=8, decimal_places=3)
    consumo = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return "%s / %s - %s" % (self.hidrometro, self.data_medicao, self.medicao)

    class Meta:
        get_latest_by = 'cmpt__competencia'

    def medicao_anterior(self, data, hidrometro):
        ret = None
        col = Medicao.objects.filter(hidrometro__id=hidrometro, cmpt__competencia__lt=data)
        if col:
            ret = col.latest()
        return ret

    def save(self, *args, **kwargs):
        mea = self.medicao_anterior(self.cmpt.competencia, self.hidrometro.id)
        medicao_ant = 0
        if mea:
            print("medica  o anterior ", mea.medicao)
            medicao_ant = (mea.medicao)

        self.consumo = self.medicao - medicao_ant
        super(Medicao, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('medicao_edit', kwargs={'pk': self.pk})


class TipoDespesa(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return "%s - %s" % (self.condominio.nome, self.descricao)

    def get_absolute_url(self):
        return reverse('tipo_despesa_edit', kwargs={'pk': self.pk})


class Despesa(models.Model):
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE)
    tipo_despesa = models.ForeignKey(TipoDespesa, on_delete=models.CASCADE)
    data_despesa = models.DateField()
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT, null=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.tipo_despesa.descricao + " [" + str(self.data_despesa) + "] " + str(self.cmpt) + " " + str(
            self.valor)

    def get_absolute_url(self):
        return reverse('despesa_edit', kwargs={'pk': self.pk})


class PagamentoCondomino(models.Model):
    condomino = models.ForeignKey(Condomino, on_delete=models.SET_NULL, null=True)
    cmpt = models.ForeignKey(Competencia, on_delete=models.PROTECT, null=True)
    data_pagamento = models.DateField(null=True, blank=True)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=18, decimal_places=2)
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super(Agua, self).save(*args,**kwargs)
