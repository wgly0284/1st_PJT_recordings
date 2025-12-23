"""
Django management command to assign keyword-based unique images to all stores
Usage: python manage.py assign_bakery_images
"""
import re
from django.core.management.base import BaseCommand
from stores.models import Store


# Keyword to image mapping (with &q=80 for better reliability)
KEYWORD_IMAGE_MAP = {
    # Cake related
    'cake|케이크|치즈케이크|티라미수': [
        "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80",
        "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600&q=80",
        "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80",
        "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600&q=80",
        "https://images.unsplash.com/photo-1574085733277-851d9d856a3a?w=600&q=80",
    ],

    # Macaron related
    'macaron|마카롱': [
        "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600&q=80",
        "https://images.unsplash.com/photo-1558312657-e4e0ff6e5eca?w=600&q=80",
        "https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=600&q=80",
    ],

    # Cookie related
    'cookie|쿠키': [
        "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600&q=80",
        "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600&q=80",
        "https://images.unsplash.com/photo-1548365328-8c6db3220e4c?w=600&q=80",
    ],

    # Donut related
    'donut|도넛': [
        "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600&q=80",
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80",
    ],

    # Croissant/Pastry
    'croissant|크루아상|페이스트리': [
        "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
        "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=600&q=80",
        "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600&q=80",
    ],

    # Bread/Bakery
    'bread|빵|식빵|바게트|호두|통밀': [
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
        "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&q=80",
        "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600&q=80",
        "https://images.unsplash.com/photo-1598373182133-52452f7691ef?w=600&q=80",
    ],

    # Pie/Tart
    'pie|tart|파이|타르트': [
        "https://images.unsplash.com/photo-1519915212116-7cfef71f1d3e?w=600&q=80",
        "https://images.unsplash.com/photo-1535920527002-b35e96722eb9?w=600&q=80",
        "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=600&q=80",
    ],

    # Bakery display
    'bakery|베이커리|제과|빵집': [
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80",
        "https://images.unsplash.com/photo-1603048297194-8f7e4d68b82a?w=600&q=80",
        "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600&q=80",
    ],
}

# Default images when no keyword matches (50+ unique images with &q=80)
DEFAULT_IMAGES = [
    # Bread displays
    "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=600&q=80",
    "https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&q=80",
    "https://images.unsplash.com/photo-1517433670267-08bbd4be890f?w=600&q=80",
    "https://images.unsplash.com/photo-1598373182133-52452f7691ef?w=600&q=80",
    "https://images.unsplash.com/photo-1549931319-a545dcf3bc73?w=600&q=80",

    # Bakery interiors
    "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600&q=80",
    "https://images.unsplash.com/photo-1603048297194-8f7e4d68b82a?w=600&q=80",
    "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=600&q=80",

    # Cakes
    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=600&q=80",
    "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=600&q=80",
    "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600&q=80",
    "https://images.unsplash.com/photo-1551024601-bec78aea704b?w=600&q=80",
    "https://images.unsplash.com/photo-1574085733277-851d9d856a3a?w=600&q=80",

    # Pastries
    "https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80",
    "https://images.unsplash.com/photo-1530610476181-d83430b64dcd?w=600&q=80",
    "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=600&q=80",

    # Cookies
    "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=600&q=80",
    "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=600&q=80",
    "https://images.unsplash.com/photo-1548365328-8c6db3220e4c?w=600&q=80",

    # Donuts
    "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600&q=80",
    "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80",

    # Macarons
    "https://images.unsplash.com/photo-1612182062631-82b605e8e34a?w=600&q=80",
    "https://images.unsplash.com/photo-1558312657-e4e0ff6e5eca?w=600&q=80",
    "https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=600&q=80",

    # Pies and tarts
    "https://images.unsplash.com/photo-1519915212116-7cfef71f1d3e?w=600&q=80",
    "https://images.unsplash.com/photo-1535920527002-b35e96722eb9?w=600&q=80",
    "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=600&q=80",

    # Additional variety
    "https://images.unsplash.com/photo-1590588469668-aae4cf6dd456?w=600&q=80",
    "https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600&q=80",
    "https://images.unsplash.com/photo-1585934034313-c77eb15c8c3f?w=600&q=80",
    "https://images.unsplash.com/photo-1607478900766-efe13248b125?w=600&q=80",
    "https://images.unsplash.com/photo-1603048297172-c92544798d5a?w=600&q=80",
    "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?w=600&q=80",
    "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600&q=80",
    "https://images.unsplash.com/photo-1617151216974-0b85f0bb3626?w=600&q=80",
    "https://images.unsplash.com/photo-1605806616949-1e87b487fc2f?w=600&q=80",
    "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?w=600&q=80",
    "https://images.unsplash.com/photo-1573141597928-403fcee0e056?w=600&q=80",
    "https://images.unsplash.com/photo-1560180445-b2298a6c0fce?w=600&q=80",
    "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=600&q=80",
    "https://images.unsplash.com/photo-1572963564891-422f4c8c5255?w=600&q=80",
    "https://images.unsplash.com/photo-1599785209796-786432b228bc?w=600&q=80",
    "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=600&q=80",
    "https://images.unsplash.com/photo-1534432182912-63863115e106?w=600&q=80",
    "https://images.unsplash.com/photo-1612182062361-cc8b5ac8c06e?w=600&q=80",
    "https://images.unsplash.com/photo-1568051243851-f9b136146e97?w=600&q=80",
    "https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?w=600&q=80",
    "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=600&q=80",
    "https://images.unsplash.com/photo-1600717794311-4154e273ca02?w=600&q=80",
]


def get_image_for_store(store_name, index):
    """
    Analyze store name and return appropriate image URL.

    Args:
        store_name: Store name
        index: Store index (for variety)

    Returns:
        Appropriate Unsplash image URL
    """
    store_name_lower = store_name.lower()

    # Keyword matching
    for keyword_pattern, images in KEYWORD_IMAGE_MAP.items():
        if re.search(keyword_pattern, store_name_lower):
            # Use index for variety within same category
            return images[index % len(images)]

    # Use default images if no keyword matches
    return DEFAULT_IMAGES[index % len(DEFAULT_IMAGES)]


class Command(BaseCommand):
    help = 'Assigns keyword-based unique images to all bakery stores'

    def handle(self, *args, **options):
        stores = Store.objects.all()
        total = stores.count()

        self.stdout.write(f"Starting to assign keyword-based images to {total} stores...\n")

        updated_count = 0
        for i, store in enumerate(stores):
            old_image = store.preview_image

            # Get keyword-based image
            new_image = get_image_for_store(store.name, i)
            store.preview_image = new_image
            store.save(update_fields=['preview_image'])

            if old_image != new_image:
                updated_count += 1

            # Progress update every 100 stores
            if (i + 1) % 100 == 0:
                self.stdout.write(f"Progress: {i + 1}/{total} completed")

        self.stdout.write(self.style.SUCCESS(f'\nCompleted!'))
        self.stdout.write(self.style.SUCCESS(f'Total stores processed: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Images updated: {updated_count}'))
