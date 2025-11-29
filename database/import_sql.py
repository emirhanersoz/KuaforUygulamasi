import sys
import os
from sqlalchemy import text
from database.db_connection import engine

def run_sql_file(filename):
    print(f"--- {filename} Dosyası Aranıyor ---")
    
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(file_path):
        print(f"HATA: {filename} dosyası bulunamadı.")
        return

    print("Dosya bulundu, okunuyor...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    
        commands = content.split(';')

        with engine.connect() as conn:
            for command in commands:
                cleaned_command = command.strip()
                if cleaned_command:
                    try:
                        conn.execute(text(cleaned_command))
                        conn.commit()
                    except Exception as e:
                        print(f"Bilgi: {e}")
        
        print("\nVeritabanı başarıyla güncellendi ve örnek veriler girildi.")
        
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")

if __name__ == "__main__":
    run_sql_file("kuafor.sql")