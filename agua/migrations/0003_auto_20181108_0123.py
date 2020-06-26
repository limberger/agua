# Generated by Django 2.1.2 on 2018-11-08 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('agua', '0002_auto_20181107_2141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competencia', models.DateField()),
                ('data_fechamento', models.DateField()),
                ('situacao', models.CharField(choices=[('AB', 'Open'), ('FC', 'Closed')], default='AB', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='PagamentoCondomino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competencia', models.DateField()),
                ('data_pagamento', models.DateField()),
                ('descricao', models.CharField(max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=18)),
                ('cmpt',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='agua.Competencia')),
                ('condominoDoCondominio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                            to='agua.CondominoDoCondominio')),
            ],
        ),
        migrations.AddField(
            model_name='despesa',
            name='cmpt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='agua.Competencia'),
        ),
        migrations.AddField(
            model_name='medicao',
            name='cmpt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='agua.Competencia'),
        ),
    ]
