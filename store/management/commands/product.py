import requests
from django.core.management.base import BaseCommand
from store.models import Categories, Product
from django.utils.text import slugify
from decimal import Decimal
import random
from dotenv import load_dotenv
import os
load_dotenv()

UNSPLASH_ACCESS_KEY =  os.getenv("UP_ACCESS") 

CATEGORY_DATA = [
    ('Electronics', 'electronics', 'laptop'),
    ('Books', 'books', 'book'),
    ('Clothing', 'clothing', 'tshirt'),
    ('Home Appliances', 'home-appliances', 'microwave'),
    ('Footwear', 'footwear', 'shoes'),
    ('Watches', 'watches', 'watch'),
    ('Toys', 'toys', 'toy'),
    ('Furniture', 'furniture', 'sofa'),
    ('Gaming', 'gaming', 'gaming'),
    ('Beauty', 'beauty', 'makeup')
]

def fetch_unsplash_image(query):
    url = "https://api.unsplash.com/photos/random"
    params = {
        'query': query,
        'orientation': 'landscape',
        'client_id': UNSPLASH_ACCESS_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return data['urls']['regular']
    except:
        return 'https://via.placeholder.com/800x600?text=Image+Not+Found'


class Command(BaseCommand):
    help = 'Delete all existing categories/products and add 100 demo products with real Unsplash images'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting existing products and categories...")
        Product.objects.all().delete()
        Categories.objects.all().delete()

        self.stdout.write("Creating new categories and products...")
        category_objs = []
        for name, slug, query in CATEGORY_DATA:
            category = Categories.objects.create(name=name, slug=slug)
            category_objs.append((category, query))

        for i in range(1, 26):
            category, query = random.choice(category_objs)
            name = f"{category.name} Product {i}"
            price = round(Decimal(random.uniform(100, 10000)), 2)
            discount = round(Decimal(random.uniform(5, 40)), 2)
            stock = random.randint(5, 100)
            slug = slugify(f"{name}-{i}")
            img_url = fetch_unsplash_image(query)
            description = f"This is a high-quality, reliable and best-in-class {name.lower()}. " \
                          f"Ideal for daily use and made with excellent materials. Comes with warranty and great support. " \
                          f"Highly rated and recommended by users across the world."

            Product.objects.create(
                name=name,
                description=description,
                price=price,
                discount=discount,
                category=category,
                stock=stock,
                is_available=True,
                slug=slug,
                img_url=img_url
            )

            self.stdout.write(self.style.SUCCESS(f'✔ Created: {name}'))

        self.stdout.write(self.style.SUCCESS('✅ Successfully added 25 products with real images.'))
