# Generated by Django 4.2.16 on 2024-12-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_customuser_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Ваша аватарка",
                null=True,
                upload_to="uploads/profile_images/",
                verbose_name="аватарка",
            ),
        ),
    ]
