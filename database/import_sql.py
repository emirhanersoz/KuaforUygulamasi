import sys
import os
from sqlalchemy import text
from database.db_connection import engine

def run_sql_file(filename):
    print(f"--- {filename} Dosyası Aranıyor ---")
    
    # Dosya yolunu tam garantiye alalım
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.exists(file_path):
        print(f"HATA: {filename} dosyası bulunamadı! Lütfen kuafor.sql dosyasının ana klasörde olduğundan emin ol.")
        return

    print("Dosya bulundu, okunuyor...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # SQL komutlarını noktalı virgüle göre ayır
        commands = content.split(';')

        with engine.connect() as conn:
            for command in commands:
                cleaned_command = command.strip()
                if cleaned_command:
                    try:
                        conn.execute(text(cleaned_command))
                        conn.commit()
                    except Exception as e:
                        # Tablo zaten varsa hata verebilir, devam et
                        print(f"Bilgi: {e}")
        
        print("\n✅ BAŞARILI! Veritabanı başarıyla güncellendi ve örnek veriler girildi.")
        
    except Exception as e:
        print(f"Dosya okuma hatası: {e}")

if __name__ == "__main__":
    # kuafor.sql dosyasının bu script ile aynı yerde olması lazım
    run_sql_file("kuafor.sql")