import json
import io
import urllib.request
from pyairtable import Api
from PIL import Image

# 1. مفاتيح واشتراك Airtable الخاصة بك
AIRTABLE_TOKEN = "patJx9M1VHnGmund3.784d44835d5c09e40503967b01ae9d0aa9b9678ad4c49798d427cb87c88acd87"
BASE_ID = "appR7VrZ8mMWNI0tQ"
TABLE_NAME = "Table 1"

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

def fetch_all_products():
    """جلب جميع البيانات من جدول Airtable أونلاين"""
    try:
        records = table.all()
        products_list = []
        
        for record in records:
            fields = record.get('fields', {})
            attachments = fields.get('الصورة', [])
            image_url = attachments[0]['url'] if attachments else ""
            
            product = {
                'id': record['id'],
                'name': fields.get('اسم المنتج', ''),
                'category': fields.get('القسم', 'عام'),
                'price': fields.get('السعر', 0),
                'image_url': image_url
            }
            products_list.append(product)
            
        return products_list
    except Exception as e:
        print("حدث خطأ أثناء جلب البيانات من Airtable:", e)
        return []

def export_to_json():
    """حفظ المنتجات في ملف json للاستخدام المحلي"""
    products = fetch_all_products()
    with open("products_data.json", "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"تم تصدير {len(products)} منتج بنجاح إلى ملف products_data.json")

if __name__ == "__main__":
    export_to_json()