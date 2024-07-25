# Generated by Django 4.2.7 on 2024-01-03 08:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant_app", "0005_alter_order_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name="product",
            name="product_name",
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]