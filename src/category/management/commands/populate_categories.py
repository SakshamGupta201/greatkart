# your_app/management/commands/populate_categories.py

import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from category.models import Category


class Command(BaseCommand):
    help = "Populate the database with dummy categories"

    def handle(self, *args, **kwargs):
        categories = [
            {
                "name": "Electronics",
                "slug": "electronics",
                "description": "Electronic items",
                "image_url": "https://cdn.prod.website-files.com/5f79627438725900eaa25c6f/65f264196e625404ede87b25_ikH0512VKiq8Jxo9dRxF093EBZP1MMtvelaM3BywVEkvrAQJA-out-0.png",
            },
            {
                "name": "Fashion",
                "slug": "fashion",
                "description": "Clothing and accessories",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQh9cb5-111zhmCSqwXEli-CEC3zF-GQDQ55A&s",
            },
            {
                "name": "Home & Kitchen",
                "slug": "home-kitchen",
                "description": "Home and kitchen appliances",
                "image_url": "https://example.com/home_kitchen.jpg",
            },
            {
                "name": "Books",
                "slug": "books",
                "description": "Books and literature",
                "image_url": "https://placehold.co/600x400",
            },
            {
                "name": "Sports",
                "slug": "sports",
                "description": "Sports equipment and accessories",
                "image_url": "https://placehold.co/600x400",
            },
        ]

        for category_data in categories:
            image_url = category_data.pop("image_url")
            category, created = Category.objects.get_or_create(**category_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created category: {category.name}"
                    )
                )
                # Download and save the image
                image_path = self.download_image(image_url, category.slug)
                category.image.save(
                    os.path.basename(image_path), File(open(image_path, "rb"))
                )
                category.save()
            else:
                self.stdout.write(
                    self.style.WARNING(f"Category already exists: {category.name}")
                )

    def download_image(self, url, slug):
        response = requests.get(url)
        image_path = os.path.join(settings.MEDIA_ROOT, "category", f"{slug}.jpg")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
