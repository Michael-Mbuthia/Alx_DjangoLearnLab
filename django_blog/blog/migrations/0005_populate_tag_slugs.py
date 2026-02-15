from django.db import migrations
from django.utils.text import slugify


def populate_tag_slugs(apps, schema_editor):
    Tag = apps.get_model('blog', 'Tag')

    for tag in Tag.objects.all().order_by('id'):
        if tag.slug:
            continue

        base = (slugify(tag.name)[:50] or 'tag')
        slug = base
        suffix = 2

        while Tag.objects.filter(slug=slug).exclude(pk=tag.pk).exists():
            slug = f"{base}-{suffix}"
            suffix += 1

        tag.slug = slug
        tag.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag_slug'),
    ]

    operations = [
        migrations.RunPython(populate_tag_slugs, migrations.RunPython.noop),
    ]
