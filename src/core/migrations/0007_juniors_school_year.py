from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190917_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='juniorscontactsubmission',
            name='child_school_year',
            field=models.CharField(choices=[('Y1', 'Year 1'), ('Y2', 'Year 2'), ('Y3', 'Year 3'), ('Y4', 'Year 4'), ('Y5', 'Year 5'), ('Y6', 'Year 6'), ('Y7', 'Year 7'), ('Y8', 'Year 8'), ('Y9', 'Year 9'), ('Y10', 'Year 10'), ('Y11', 'Year 11')], default='', max_length=10, verbose_name='School year'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='juniorscontactsubmission',
            name='child_age',
            field=models.CharField(choices=[('A6', '6'), ('A7', '7'), ('A8', '8'), ('A9', '9'), ('A10', '10'), ('A11', '11'), ('A12', '12'), ('A13', '13'), ('A14', '14'), ('A15', '15'), ('A16', '16')], max_length=10),
        ),
        migrations.AlterField(
            model_name='juniorscontactsubmission',
            name='child_gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
