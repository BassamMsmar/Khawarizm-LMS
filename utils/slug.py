def generate_arabic_slug(text):
    allowed_chars = ''.join(c for c in text if c.isalnum() or c.isspace())
    return '-'.join(allowed_chars.split()) or 'item'

def get_unique_slug(model_class, field_value, instance=None):
    base_slug = generate_arabic_slug(field_value)
    slug = base_slug
    counter = 1
    qs = model_class.objects
    if instance:
        qs = qs.exclude(pk=instance.pk)
    while qs.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug
