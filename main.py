import argparse
import json
from pathlib import Path

def add_expense(amount: float, category: str, expense_type: str):
    file_path = Path("expenses.json")
    
    # 1. Eğer dosya varsa içindeki eski verileri oku, yoksa boş liste oluştur
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # 2. Yeni veriyi bir sözlük (dict) olarak hazırla
    new_entry = {
        "amount": amount,
        "category": category.strip().lower(),
        "type": expense_type
    }

    # 3. Yeni veriyi listenin sonuna ekle
    data.append(new_entry)

    # 4. Güncel listeyi JSON dosyasına geri yaz
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f" Başarıyla eklendi: {amount} TL - {category} ({expense_type})")


def list_expenses():
    file_path = Path("expenses.json")
    if not file_path.exists():
        print("Henüz hiç kayıt bulunamadı.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        
    print("\n--- KAYITLI HARCAMA VE GELİRLER ---")
    for idx, item in enumerate(data, 1):
        print(f"{idx}. [{item['type'].upper()}] {item['category']}: {item['amount']} TL")


def show_total():
    file_path = Path("expenses.json")
    if not file_path.exists():
        print("Henüz hiç kayıt bulunamadı.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # List Comprehension ile gelir ve giderleri ayıklıyoruz
    expenses = [item["amount"] for item in data if item["type"] == "expense"]
    incomes = [item["amount"] for item in data if item["type"] == "income"]

    total_expense = sum(expenses)
    total_income = sum(incomes)
    net_balance = total_income - total_expense

    print(f"\n Toplam Gelir: {total_income} TL")
    print(f" Toplam Gider: {total_expense} TL")
    print(f" Net Durum: {net_balance} TL")


def main():
    # 1. Ana argüman yöneticisini oluşturuyoruz
    parser = argparse.ArgumentParser(description="Haftalık Gider Takip Sistemi")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 2. "add" komutunu tanımlıyoruz
    add_parser = subparsers.add_parser("add", help="Yeni bir gelir veya gider ekler")
    add_parser.add_argument("--amount", type=float, required=True, help="Miktar (Örn: 150.50)")
    add_parser.add_argument("--category", type=str, required=True, help="Kategori (Örn: Yemek, Fatura)")
    add_parser.add_argument("--type", type=str, choices=["income", "expense"], required=True, help="Tür: income veya expense")

    # 3. "list" ve "total" komutlarını buraya, yani main içine tanımlıyoruz
    subparsers.add_parser("list", help="Tüm kayıtları listeler")
    subparsers.add_parser("total", help="Toplam harcama miktarını gösterir")

    # 4. Terminalden gelen argümanları çözümlüyoruz
    args = parser.parse_args()

    # Komut kontrolü
    if args.command == "add":
        add_expense(args.amount, args.category, args.type)
    elif args.command == "list":
        list_expenses()
    elif args.command == "total":
        show_total()

if __name__ == "__main__":
    main()