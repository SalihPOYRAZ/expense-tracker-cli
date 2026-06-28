import argparse
import json
from pathlib import Path

def add_expense(amount: float, category: str, expense_type: str):
    file_path = Path("expenses.json")
    
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    new_entry = {
        "amount": amount,
        "category": category.strip().lower(),
        "type": expense_type
    }

    data.append(new_entry)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f" Başarıyla eklendi: {amount} TL - {category} ({expense_type})")

def list_expenses():
    file_path = Path("expenses.json")
    if not file_path.exists():
        print("Henüz hiç kayıt bulunamadı.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print("Veri dosyası bozuk veya okunamıyor.")
            return
        
    print("\n--- KAYITLI HARCAMA VE GELİRLER ---")
    for idx, item in enumerate(data, 1):
        print(f"{idx}. [{item['type'].upper()}] {item['category']}: {item['amount']} TL")

def filter_by_category(category_name: str):
    file_path = Path("expenses.json")
    if not file_path.exists():
        print("Henüz hiç kayıt bulunamadı.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    search_term = category_name.strip().lower()
    filtered_data = [item for item in data if item["category"] == search_term]

    if not filtered_data:
        print(f"'{category_name}' kategorisine ait hiçbir kayıt bulunamadı.")
        return

    print(f"\n--- '{category_name.upper()}' KATEGORİSİNDEKİ KAYITLAR ---")
    for idx, item in enumerate(filtered_data, 1):
        print(f"{idx}. [{item['type'].upper()}] {item['amount']} TL")

def show_total():
    file_path = Path("expenses.json")
    if not file_path.exists():
        print("Henüz hiç kayıt bulunamadı.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    total_income = sum(item["amount"] for item in data if item["type"] == "income")
    total_expense = sum(item["amount"] for item in data if item["type"] == "expense")

    print(f"\n--- TOPLAM GELİR VE GİDER ---")
    print(f"Toplam Gelir: {total_income} TL")
    print(f"Toplam Gider: {total_expense} TL")
    print(f"Net Bakiye: {total_income - total_expense} TL")

def main():
    parser = argparse.ArgumentParser(description="Haftalık Gider Takip Sistemi")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 1. Bütün komut tanımlamalarını eksiksiz yapıyoruz
    add_parser = subparsers.add_parser("add", help="Yeni bir gelir veya gider ekler")
    add_parser.add_argument("--amount", type=float, required=True, help="Miktar (Örn: 150.50)")
    add_parser.add_argument("--category", type=str, required=True, help="Kategori (Örn: Yemek, Fatura)")
    add_parser.add_argument("--type", type=str, choices=["income", "expense"], required=True, help="Tür: income veya expense")

    subparsers.add_parser("list", help="Tüm kayıtları listeler")
    subparsers.add_parser("total", help="Toplam harcama miktarını gösterir")

    category_parser = subparsers.add_parser("by-category", help="Kategoriye göre harcamaları filtreler")
    category_parser.add_argument("--name", type=str, required=True, help="Filtrelenecek kategori adı (Örn: yemek)")

    # PLANINDAKİ EN KRİTİK NOKTA: Kullanıcı geçersiz miktar girerse oluşacak hatayı try-except ile yakalıyoruz
    try:
        args = parser.parse_args()
    except SystemExit:
        # Argparse hatalı girişte otomatik olarak SystemExit fırlatır, programın çirkin çökmesini önlemek için yakalıyoruz
        return

    # 2. Komut eşleşmelerini yönlendiriyoruz
    if args.command == "add":
        add_expense(args.amount, args.category, args.type)
    elif args.command == "list":
        list_expenses()
    elif args.command == "total":
        show_total()
    elif args.command == "by-category":
        filter_by_category(args.name)

if __name__ == "__main__":
    main()