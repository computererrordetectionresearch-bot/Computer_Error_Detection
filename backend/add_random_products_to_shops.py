"""
Add random products to every category for every shop.
Ensures each shop has at least one product in each category.
"""

from pathlib import Path
import pandas as pd
import random
import sys
import io
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HERE = Path(__file__).parent.resolve()
DATA_DIR = (HERE.parent / "data").resolve()
PRODUCTS_CSV = DATA_DIR / "products.csv"
SHOPS_CSV = DATA_DIR / "shops.csv"

# Product categories
CATEGORIES = ["Motherboard", "SSD", "Laptop", "GPU", "Monitor", "CPU", "RAM", "PSU"]

# Brand and model combinations by category
PRODUCT_TEMPLATES = {
    "Motherboard": [
        ("MSI", "B450", "B450 chipset, Mini-ITX"),
        ("ASUS", "Z690", "Z690 chipset, mATX"),
        ("Gigabyte", "X570", "X570 chipset, ATX"),
        ("ASRock", "B550", "B550 chipset, Mini-ITX"),
        ("MSI", "Z690", "Z690 chipset, ATX"),
        ("ASUS", "B450", "B450 chipset, mATX"),
        ("Gigabyte", "B550", "B550 chipset, ATX"),
        ("MSI", "X570", "X570 chipset, Mini-ITX"),
    ],
    "SSD": [
        ("Crucial", "250GB", "250GB, SATA"),
        ("Samsung", "500GB", "500GB, NVMe PCIe 4.0"),
        ("Kingston", "1TB", "1TB, SATA"),
        ("Adata", "2TB", "2TB, NVMe PCIe 4.0"),
        ("Crucial", "500GB", "500GB, SATA"),
        ("Samsung", "1TB", "1TB, NVMe PCIe 4.0"),
        ("Kingston", "2TB", "2TB, SATA"),
        ("Adata", "250GB", "250GB, NVMe PCIe 4.0"),
    ],
    "Laptop": [
        ("HP", "Pavilion", "16GB RAM, 512GB SSD, i5"),
        ("Dell", "Inspiron", "8GB RAM, 256GB SSD, i5"),
        ("ASUS", "VivoBook", "16GB RAM, 512GB SSD, Ryzen 5"),
        ("Lenovo", "ThinkPad", "32GB RAM, 1024GB SSD, i7"),
        ("Acer", "Aspire", "8GB RAM, 256GB SSD, Ryzen 5"),
        ("Apple", "MacBook Air", "16GB RAM, 512GB SSD, M1"),
        ("MSI", "GF63", "16GB RAM, 1024GB SSD, i5"),
        ("HP", "EliteBook", "32GB RAM, 512GB SSD, Ryzen 7"),
    ],
    "GPU": [
        ("NVIDIA", "RTX 3060", "12GB GDDR6, Dual Fan"),
        ("AMD", "RX 6600", "8GB GDDR6, Triple Fan"),
        ("Gigabyte", "RTX 4070", "12GB GDDR6, Dual Fan"),
        ("Zotac", "RTX 3070", "8GB GDDR6, Triple Fan"),
        ("ASUS", "RTX 3060", "12GB GDDR6, Dual Fan"),
        ("MSI", "RX 6800", "16GB GDDR6, Triple Fan"),
        ("NVIDIA", "GTX 1660", "6GB GDDR6, Dual Fan"),
        ("AMD", "RTX 4070", "12GB GDDR6, Dual Fan"),
    ],
    "Monitor": [
        ("LG", "24-inch FHD", "24-inch FHD, 75Hz"),
        ("Dell", "27-inch QHD", "27-inch QHD, 240Hz"),
        ("BenQ", "32-inch 4K", "32-inch 4K, 144Hz"),
        ("ASUS", "24-inch FHD", "24-inch FHD, 144Hz"),
        ("AOC", "27-inch QHD", "27-inch QHD, 165Hz"),
        ("Samsung", "32-inch 4K", "32-inch 4K, 120Hz"),
        ("LG", "27-inch QHD", "27-inch QHD, 144Hz"),
        ("BenQ", "24-inch FHD", "24-inch FHD, 75Hz"),
    ],
    "CPU": [
        ("Intel", "i5-12400F", "Intel i5-12400F, 12 cores"),
        ("AMD", "Ryzen 5 5600X", "AMD Ryzen 5 5600X, 6 cores"),
        ("Intel", "i7-13700K", "Intel i7-13700K, 6 cores"),
        ("AMD", "Ryzen 7 5800X", "AMD Ryzen 7 5800X, 8 cores"),
        ("Intel", "i5-12400", "Intel i5-12400, 12 cores"),
        ("AMD", "Ryzen 9 5900X", "AMD Ryzen 9 5900X, 12 cores"),
        ("Intel", "i9-13900K", "Intel i9-13900K, 24 cores"),
        ("AMD", "Ryzen 5 5600", "AMD Ryzen 5 5600, 6 cores"),
    ],
    "RAM": [
        ("Crucial", "8GB DDR4", "8GB DDR4, 3200MHz"),
        ("Kingston", "16GB DDR4", "16GB DDR4, 3600MHz"),
        ("Corsair", "32GB DDR4", "32GB DDR4, 3200MHz"),
        ("G.Skill", "16GB DDR5", "16GB DDR5, 3600MHz"),
        ("TeamGroup", "8GB DDR4", "8GB DDR4, 2666MHz"),
        ("Crucial", "16GB DDR5", "16GB DDR5, 3600MHz"),
        ("Kingston", "32GB DDR4", "32GB DDR4, 3600MHz"),
        ("Corsair", "16GB DDR4", "16GB DDR4, 3200MHz"),
    ],
    "PSU": [
        ("Cooler Master", "650W", "650W, 80+ Gold"),
        ("Thermaltake", "750W", "750W, 80+ Gold"),
        ("Seasonic", "850W", "850W, 80+ Bronze"),
        ("EVGA", "550W", "550W, 80+ Platinum"),
        ("Corsair", "750W", "750W, 80+ Gold"),
        ("Thermaltake", "850W", "850W, 80+ Platinum"),
        ("Cooler Master", "550W", "550W, 80+ Bronze"),
        ("Seasonic", "650W", "650W, 80+ Gold"),
    ],
}

# Price ranges by category (in LKR)
PRICE_RANGES = {
    "Motherboard": (50000, 200000),
    "SSD": (5000, 50000),
    "Laptop": (80000, 500000),
    "GPU": (50000, 800000),
    "Monitor": (30000, 200000),
    "CPU": (20000, 300000),
    "RAM": (3000, 50000),
    "PSU": (5000, 50000),
}

# Stock status options
STOCK_STATUS = ["In Stock", "Out of Stock"]
WARRANTY_OPTIONS = ["6 Months", "12 Months", "24 Months", "36 Months"]
VERIFIED_OPTIONS = ["Yes", "No", "Maybe"]

def generate_product_id(existing_ids, counter):
    """Generate unique product ID."""
    while True:
        product_id = f"P{str(counter).zfill(4)}"
        if product_id not in existing_ids:
            return product_id
        counter += 1

def add_random_products():
    """Add random products to every category for every shop."""
    print("=" * 80)
    print("ADDING RANDOM PRODUCTS TO ALL SHOPS")
    print("=" * 80)
    
    # Load existing products
    print("\n[INFO] Loading existing products...")
    df_products = pd.read_csv(PRODUCTS_CSV)
    print(f"[INFO] Loaded {len(df_products)} existing products")
    
    # Load shops
    print("\n[INFO] Loading shops...")
    df_shops = pd.read_csv(SHOPS_CSV)
    print(f"[INFO] Loaded {len(df_shops)} shops")
    
    # Get unique shop_ids from products (only product_shop type)
    existing_shop_ids = set(df_products[df_products['shop_type'] == 'product_shop']['shop_id'].unique())
    all_shop_ids = set(df_shops['shop_id'].unique())
    
    # Get shops that need products
    shops_to_process = all_shop_ids if len(all_shop_ids) > len(existing_shop_ids) else existing_shop_ids
    
    print(f"\n[INFO] Processing {len(shops_to_process)} shops")
    print(f"[INFO] Categories to add: {CATEGORIES}")
    
    # Get existing product IDs
    existing_product_ids = set(df_products['product_id'].unique())
    product_counter = max([int(pid[1:]) for pid in existing_product_ids if pid.startswith('P') and pid[1:].isdigit()], default=0) + 1
    
    new_products = []
    
    # For each shop, check which categories they have and add missing ones
    for shop_id in shops_to_process:
        shop_info = df_shops[df_shops['shop_id'] == shop_id]
        if shop_info.empty:
            continue
        
        shop_row = shop_info.iloc[0]
        shop_name = shop_row['shop_name']
        district = shop_row['district']
        
        # Get existing categories for this shop
        shop_products = df_products[df_products['shop_id'] == shop_id]
        existing_categories = set(shop_products['category'].unique())
        
        # Add products for missing categories
        for category in CATEGORIES:
            if category not in existing_categories:
                # Generate random product
                brand, model, specs = random.choice(PRODUCT_TEMPLATES[category])
                price = random.randint(*PRICE_RANGES[category])
                stock_status = random.choice(STOCK_STATUS)
                warranty = random.choice(WARRANTY_OPTIONS)
                verified = random.choice(VERIFIED_OPTIONS)
                
                product_id = generate_product_id(existing_product_ids, product_counter)
                existing_product_ids.add(product_id)
                product_counter += 1
                
                # Create product entry for product_shop
                new_product = {
                    'product_id': product_id,
                    'shop_id': shop_id,
                    'shop_name': shop_name,
                    'district': district,
                    'category': category,
                    'brand': brand,
                    'model': model,
                    'specifications': specs,
                    'price_lkr': price,
                    'stock_status': stock_status,
                    'warranty': warranty,
                    'last_updated': datetime.now().strftime('%Y-%m-%d'),
                    'verified': verified,
                    'shop_name_shop': shop_name,
                    'district_shop': district,
                    'city_address': shop_row.get('city_address', ''),
                    'latitude': shop_row.get('latitude', ''),
                    'longitude': shop_row.get('longitude', ''),
                    'average_rating': shop_row.get('average_rating', 5.0),
                    'reviews_count': shop_row.get('reviews_count', 0),
                    'verified_shop': shop_row.get('verified', 'Maybe'),
                    'shop_type': 'product_shop'
                }
                new_products.append(new_product)
                
                # Also create entry for a random repair_shop in the same district
                repair_shops = df_shops[
                    (df_shops['district'] == district) & 
                    (df_shops['shop_type'] == 'repair_shop')
                ]
                if not repair_shops.empty:
                    repair_shop = repair_shops.sample(1).iloc[0]
                    repair_product = new_product.copy()
                    repair_product['shop_name_shop'] = repair_shop['shop_name']
                    repair_product['district_shop'] = repair_shop['district']
                    repair_product['city_address'] = repair_shop.get('city_address', '')
                    repair_product['latitude'] = repair_shop.get('latitude', '')
                    repair_product['longitude'] = repair_shop.get('longitude', '')
                    repair_product['average_rating'] = repair_shop.get('average_rating', 5.0)
                    repair_product['reviews_count'] = repair_shop.get('reviews_count', 0)
                    repair_product['verified_shop'] = repair_shop.get('verified', 'Maybe')
                    repair_product['shop_type'] = 'repair_shop'
                    new_products.append(repair_product)
    
    if not new_products:
        print("\n[INFO] All shops already have products in all categories!")
        return
    
    # Create DataFrame from new products
    df_new = pd.DataFrame(new_products)
    
    # Combine with existing products
    df_combined = pd.concat([df_products, df_new], ignore_index=True)
    
    # Save
    df_combined.to_csv(PRODUCTS_CSV, index=False, encoding='utf-8')
    
    print(f"\n[SUCCESS] Added {len(new_products)} new products")
    print(f"[INFO] Total products: {len(df_combined)}")
    print(f"[INFO] Products saved to: {PRODUCTS_CSV}")
    
    # Show summary
    print(f"\n[INFO] Category distribution in new products:")
    print(df_new['category'].value_counts())
    
    print(f"\n[INFO] Products per shop (sample):")
    shop_counts = df_combined.groupby('shop_id')['category'].nunique()
    print(f"  Average categories per shop: {shop_counts.mean():.1f}")
    print(f"  Min categories: {shop_counts.min()}")
    print(f"  Max categories: {shop_counts.max()}")

if __name__ == "__main__":
    add_random_products()

