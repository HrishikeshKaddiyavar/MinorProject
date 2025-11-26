# food/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from food.models import MenuItem, Category

class Command(BaseCommand):
    help = 'Seeds the database with initial menu categories and items.'

    def handle(self, *args, **options):
        # 1. Clear existing data to prevent duplicates on re-run
        MenuItem.objects.all().delete()
        Category.objects.all().delete()

        # 2. Define data
        initial_categories = ['Appetizers', 'Main Course', 'Desserts', 'Beverages']
        categories_map = {}
        for cat_name in initial_categories:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories_map[cat_name] = category
            self.stdout.write(self.style.SUCCESS(f'Category: {cat_name} created/found.'))

        menu_data = [
            {'name': 'Butter Chicken', 'category': 'Main Course', 'price': 350, 'image': '🍛', 'description': 'Creamy tomato-based curry', 'available': True},
            {'name': 'Paneer Tikka', 'category': 'Appetizers', 'price': 250, 'image': '🧀', 'description': 'Grilled cottage cheese', 'available': True},
            {'name': 'Biryani', 'category': 'Main Course', 'price': 400, 'image': '🍚', 'description': 'Aromatic rice with spices', 'available': True},
            {'name': 'Samosa', 'category': 'Appetizers', 'price': 50, 'image': '🥟', 'description': 'Crispy fried pastry', 'available': True},
            {'name': 'Gulab Jamun', 'category': 'Desserts', 'price': 100, 'image': '🍡', 'description': 'Sweet milk solids', 'available': True},
            {'name': 'Masala Dosa', 'category': 'Main Course', 'price': 180, 'image': '🥞', 'description': 'South Indian crepe', 'available': True},
            {'name': 'Mango Lassi', 'category': 'Beverages', 'price': 120, 'image': '🥤', 'description': 'Yogurt mango drink', 'available': True},
            {'name': 'Tandoori Chicken', 'category': 'Main Course', 'price': 380, 'image': '🍗', 'description': 'Clay oven roasted', 'available': True},
        ]
        
        # 3. Insert Menu Items
        for item in menu_data:
            MenuItem.objects.create(
                name=item['name'],
                category=categories_map[item['category']],
                price=item['price'],
                image=item['image'],
                description=item['description'],
                available=item['available'],
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded initial menu data.'))