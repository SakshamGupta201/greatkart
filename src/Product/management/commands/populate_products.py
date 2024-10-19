# your_app/management/commands/populate_products.py

import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from faker import Faker
from Product.models import Product, Category
import requests


class Command(BaseCommand):
    help = "Populate the database with dummy products"

    def handle(self, *args, **kwargs):
        fake = Faker("en_US")
        categories = Category.objects.all()

        for _ in range(50):  # Number of products to create
            category = random.choice(categories)
            product = Product.objects.create(
                name=fake.word(),
                slug=fake.slug(),
                description=fake.text(),
                price=round(random.uniform(10.0, 100.0), 2),
                stock=random.randint(1, 100),
                category=category,
                image=self.download_image(fake.image_url(), fake.slug()),
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created product: {product.name}")
            )

    def download_image(self, url, slug):
        response = requests.get(url)
        image_path = os.path.join(settings.MEDIA_ROOT, "products", f"{slug}.jpg")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
