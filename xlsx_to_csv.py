import pandas as pd
import re
import os
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def clean_name(sheet_name):
    # Remove caracters speciais e espaços usando regex das abas
    cleaned_name = re.sub(r'[^\w\s]', '', sheet_name)
    cleaned_name = re.sub(r'\s+', '_', cleaned_name)
    cleaned_name = remove_accents(cleaned_name)
    return cleaned_name


def xlsx_to_csv(input_file, output_file, filename):
    # Load the Excel file
    csv_files_names_withoutpath = []
    output_file = output_file.replace(".xlsx", "")
    filename = filename.replace(".xlsx", "")
    xls = pd.ExcelFile(input_file)
    # Pega as abas do Excel
    sheet_names = xls.sheet_names
    # Itera cada aba e salva como CSV
    for sheet_name in sheet_names:
        # Carrega as abas como DataFrame
        df = xls.parse(sheet_name, skiprows=range(1, 2))
        # Nomes das abas limpas
        cleaned_sheet_name=clean_name(sheet_name)
        # Nome das colunas limpas
        df.columns = [clean_name(col) for col in df.columns]
        # Nome do CSV
        csv_file_name=f"{output_file}_{sheet_name}.csv"
        # Salva o Dataframe como CSV
        df.to_csv(csv_file_name, index=False)
        # Corrige o nome se tiver caracter especial
        if os.path.exists(csv_file_name):
            new_csv_file_name=f"{output_file}_{cleaned_sheet_name}.csv"
            try:
                os.rename(csv_file_name, new_csv_file_name)
            except Exception:
                if os.path.exists(new_csv_file_name):
                    os.remove(new_csv_file_name)
                    os.rename(csv_file_name, new_csv_file_name)
        csv_files_names_withoutpath.append(
            f"{filename}_{cleaned_sheet_name}.csv")
    return csv_files_names_withoutpath
