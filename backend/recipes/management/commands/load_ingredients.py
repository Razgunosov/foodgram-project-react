import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.import_ingredients()
        print('Импорт прошёл успешно.')

    def import_ingredients(self, file='ingredients.csv'):
        print(f'Загрузка {file}...')
        file_path = f'./data/{file}'
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            ingredients = [
                Ingredient(
                    name=row[0],
                    measurement_unit=row[1],
                )
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients)
