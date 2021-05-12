from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_especie', models.CharField(default='-', help_text='Seleccione la especie', max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Especie',
                'verbose_name_plural': 'Especies',
            },
        ),
        migrations.CreateModel(
            name='FichaMedica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_create', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ficha Medica',
                'verbose_name_plural': 'Fichas Medicas',
            },
        ),
        migrations.CreateModel(
            name='HistoricoFichaMedica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacuna', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('tipo_vacuna', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('proxima_vacunacion', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('diagnostico', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('tratamiento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('proximo_tratamiento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('medicamento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('fecha_ultima_consulta', models.DateField(blank=True, null=True)),
                ('fecha_proxima_consulta', models.DateField(blank=True, null=True)),
                ('antiparasitario', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('proximo_antiparasitario', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('peso', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('id_ficha_medica', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Historico Ficha Medicas',
                'verbose_name_plural': 'Historicos Fichas Medicas',
            },
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacuna', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('tipo_vacuna', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('proxima_vacunacion', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('id_ficha_medica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.fichamedica')),
            ],
            options={
                'verbose_name': 'Ficha Medica',
                'verbose_name_plural': 'Fichas Medicas',
            },
        ),
        migrations.CreateModel(
            name='Raza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_raza', models.CharField(default='-', help_text='Seleccione la raza', max_length=200)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('id_especie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.especie')),
            ],
            options={
                'verbose_name': 'Raza',
                'verbose_name_plural': 'Razas',
            },
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_mascota', models.CharField(help_text='Ingrese nombre de la mascota', max_length=200)),
                ('tatuaje', models.CharField(blank=True, default='-', help_text='Ingrese el tatuaje', max_length=200, null=True)),
                ('sexo', models.CharField(choices=[('MAC', 'Macho'), ('HEB', 'Hembra')], default='-', help_text='Seleccione el sexo', max_length=15)),
                ('edad', models.CharField(blank=True, default='-', max_length=200, null=True)),
                ('imagen', models.ImageField(blank=True, help_text='Ingrese una foto', null=True, upload_to='mascotas/fotos')),
                ('peso', models.CharField(help_text='Ingrese el peso de la mascota', max_length=200)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('color_pelaje', models.CharField(blank=True, default='-', help_text='Ingrese el color de la mascota', max_length=200, null=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente')),
                ('id_raza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.raza')),
            ],
            options={
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
            },
        ),
        migrations.AddField(
            model_name='fichamedica',
            name='id_mascota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.mascota'),
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnostico', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('tratamiento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('proximo_tratamiento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('medicamento', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('fecha_ultima_consulta', models.DateField(blank=True, null=True)),
                ('fecha_proxima_consulta', models.DateField(blank=True, null=True)),
                ('id_ficha_medica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.fichamedica')),
            ],
            options={
                'verbose_name': 'Consulta',
                'verbose_name_plural': 'Consultas',
            },
        ),
        migrations.CreateModel(
            name='Antiparasitario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antiparasitario', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('proximo_antiparasitario', models.CharField(blank=True, default='-', max_length=500, null=True)),
                ('id_ficha_medica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascota.fichamedica')),
            ],
            options={
                'verbose_name': 'Antiparasitario',
                'verbose_name_plural': 'Antiparasitarios',
            },
        ),
    ]
