# Generated by Django 4.2.7 on 2023-12-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant_app", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="id",
        ),
        migrations.AlterField(
            model_name="product",
            name="product_name",
            field=models.CharField(max_length=256, primary_key=True, serialize=False),
        ),
    ]