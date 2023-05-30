# Generated by Django 4.2 on 2023-05-30 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wishes', '0007_wish_image_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='bought',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='wish',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='image_link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='link',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='wish',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='wish',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='wish',
            name='wish_list',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='wishes.wishlist'),
        ),
    ]