input_file = r'C:\Users\.Rayan.Servic.e\Desktop\prediction\data\q.txt'
output_file = r'C:\Users\.Rayan.Servic.e\Desktop\prediction\data\q_cleaned.txt'

try:

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    
    cleaned_lines = []
    for line in lines:
        stripped_line = line.strip()  
        if stripped_line:  
            cleaned_lines.append(stripped_line)

    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(" ".join(cleaned_lines))  

    print(f"فایل پردازش شد و در '{output_file}' ذخیره شد.")

except FileNotFoundError:
    print(f"Error: فایل '{input_file}' یافت نشد.")