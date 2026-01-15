import re
import os
from supabase import create_client, Client

class DatabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        self.supabase = create_client(url, key) if url and key else None

    def normalize_data(self, price_str):
        if not price_str: return 0.0
        clean_price = re.sub(r'[^\d.,]', '', price_str)
        if ',' in clean_price and '.' in clean_price:
            clean_price = clean_price.replace('.', '').replace(',', '.') if clean_price.find('.') < clean_price.find(',') else clean_price.replace(',', '')
        elif ',' in clean_price: clean_price = clean_price.replace(',', '.')
        try: return float(clean_price)
        except: return 0.0

    def insert_product(self, product_data):
        if not self.supabase: return False
        data = {
            "name": product_data.get('name'),
            "price": self.normalize_data(product_data.get('price')),
            "source": product_data.get('source'),
            "link": product_data.get('link')
        }
        try:
            self.supabase.table("product_history").insert(data).execute()
            return True
        except Exception as e:
            print(f"Error Supabase: {e}")
            return False
