def make_slug(candidate):
    slug = candidate
    slug = slug.replace(' ', '-')
    slug = slug.lower()
    return slug
