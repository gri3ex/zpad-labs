import pandas as pd
import glob
import os
import re
from io import StringIO

def parse_vhi_file(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    
    # Витягуємо назву області з першого рядка
    match = re.search(r'Province=\s*\d+:\s*([^,]+)', content[0])
    region = match.group(1).strip() if match else f"Region_{os.path.basename(file_path)}"
    
    # Очищення від HTML-тегів та зайвих ком
    clean_lines = []
    for line in content:
        clean_line = re.sub(r'<[^>]*>', '', line).strip().rstrip(',')
        if clean_line:
            clean_lines.append(clean_line)
    
    # Header на 2-му рядку, дані далі
    header = clean_lines[1]
    data = "\n".join(clean_lines[2:])
    
    df = pd.read_csv(StringIO(data), header=None, names=[col.strip() for col in header.split(',')])
    df['Region'] = region
    return df

# Шлях до папки з твоїми 27 файлами (зміни на свій, якщо треба)
path_to_files = 'vhi_data/*.csv' 
all_files = glob.glob(path_to_files)

if not all_files:
    print("Файли не знайдено! Перевір шлях до папки.")
else:
    print(f"Знайдено файлів: {len(all_files)}. Починаю об'єднання...")
    li = [parse_vhi_file(f) for f in all_files]
    final_df = pd.concat(li, ignore_index=True)
    
    # Форматування для Streamlit
    final_df = final_df.rename(columns={'year': 'Year', 'week': 'Week'})
    final_df.dropna(subset=['VHI'], inplace=True) # Прибираємо порожні рядки
    final_df['Year'] = final_df['Year'].astype(int)
    final_df['Week'] = final_df['Week'].astype(int)
    
    final_df.to_csv('vhi_data.csv', index=False)
    print("Готово! Файл vhi_data.csv створено.")