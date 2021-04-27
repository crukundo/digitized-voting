from django.db import migrations


def create_faculties(apps, schema_editor):
    Faculty = apps.get_model('institution', 'Faculty')
    Faculty.objects.create(name='General Guild', color='#343a40')
    Faculty.objects.create(name='COCIS', color='#007bff')
    Faculty.objects.create(name='COBAMS', color='#28a745')
    Faculty.objects.create(name='CEES', color='#17a2b8')
    Faculty.objects.create(name='CHS', color='#ffc107')


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_faculties),
    ]