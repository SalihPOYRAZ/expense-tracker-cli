import argparse
import json
from pathlib import Path

def add_expense(amount: float, category: str, expense_type: str):  # Type hint kullanmayı unutmuyoruz!
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
        "category": category.strip().lower(), # Standart olsun diye küçük harfe çeviriyoruz
        "type": expense_type
    }

    # 3. Yeni veriyi listenin sonuna ekle
    data.append(new_entry)

    # 4. Güncel listeyi JSON dosyasına geri yaz
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
    print(f" Başarıyla eklendi: {amount} TL - {category} ({expense_type})")



def main():
    # 1. Ana argüman yöneticisini oluşturuyoruz
    parser = argparse.ArgumentParser(description="Haftalık Gider Takip Sistemi")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 2. "add" komutunu tanımlıyoruz
    add_parser = subparsers.add_parser("add", help="Yeni bir gelir veya gider ekler")
    
    # 3. "add" komutunun isteyeceği parametreleri (argümanları) tanımlıyoruz
    add_parser.add_argument("--amount", type=float, required=True, help="Miktar (Örn: 150.50)")
    add_parser.add_argument("--category", type=str, required=True, help="Kategori (Örn: Yemek, Fatura)")
    add_parser.add_argument("--type", type=str, choices=["income", "expense"], required=True, help="Tür: income veya expense")

    # 4. Terminalden gelen argümanları parse et (oku/çözümle)
    args = parser.parse_args()

    # Eğer gelen komut "add" ise ilgili fonksiyonu çağıracağız
    if args.command == "add":
        add_expense(args.amount, args.category, args.type)

if __name__ == "__main__":
    main()

    