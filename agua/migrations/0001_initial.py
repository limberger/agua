# Generated by Django 2.1.2 on 2018-11-07 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Condominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Condomino',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_conhecido', models.CharField(max_length=50)),
                ('nome_completo', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='CondominoDoCondominio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('condominio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.Condominio')),
                ('condomino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.Condomino')),
            ],
        ),
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_despesa', models.DateField()),
                ('competencia', models.DateField()),
                ('descricao', models.CharField(max_length=200)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=18)),
                ('condominio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.Condominio')),
            ],
        ),
        migrations.CreateModel(
            name='Hidrometro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacao', models.CharField(max_length=100)),
                ('casasDecimais', models.IntegerField()),
                ('condominoDoCondominio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.CondominoDoCondominio')),
            ],
        ),
        migrations.CreateModel(
            name='Medicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_medicao', models.DateField()),
                ('competencia', models.DateField()),
                ('medicao', models.DecimalField(decimal_places=3, max_digits=8)),
                ('hidrometro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.Hidrometro')),
            ],
        ),
        migrations.CreateModel(
            name='TipoDespesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('condominio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.Condominio')),
            ],
        ),
        migrations.AddField(
            model_name='despesa',
            name='tipo_despesa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agua.TipoDespesa'),
        ),
    ]
