# Generated by Django 4.1.7 on 2023-05-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("magasin", "0036_alter_panier_options_remove_panier_client_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="produit", name="stock", field=models.IntegerField(default=0),
        ),
    ]
