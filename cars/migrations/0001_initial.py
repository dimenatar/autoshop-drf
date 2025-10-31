import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mark', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=30)),
                ('horsepower', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('year', models.IntegerField(default=1800, validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Cars',
                'verbose_name_plural': 'Cars',
            },
        ),
    ]
