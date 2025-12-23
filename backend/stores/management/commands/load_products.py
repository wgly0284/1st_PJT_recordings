import json
from django.core.management.base import BaseCommand
from stores.models import Product, Store, Keyword

class Command(BaseCommand):
    help = 'Loads products from a JSON file'

    def handle(self, *args, **kwargs):
        with open('stores/fixtures/keywords_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            fields = item['fields']
            store_id = fields.pop('store')
            keyword_names = fields.pop('keywords')
            
            try:
                store = Store.objects.get(pk=store_id)
            except Store.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Store with id "{store_id}" does not exist.'))
                continue

            product, created = Product.objects.update_or_create(
                pk=item['pk'],
                defaults={**fields, 'store': store}
            )

            for keyword_name in keyword_names:
                keyword, _ = Keyword.objects.get_or_create(name=keyword_name)
                product.keywords.add(keyword)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created product "{product.name}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Successfully updated product "{product.name}"'))
