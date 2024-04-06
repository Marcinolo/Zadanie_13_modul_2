

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="born_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="born_location",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="author",
            name="descryption",
            field=models.TextField(blank=True, null=True),
        ),
    ]
