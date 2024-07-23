import arcpy
import pandas as pd
import logging
import csv


def get_field_aliases(table_name):
    field_info = arcpy.Describe(table_name).fieldInfo
    num_fields = field_info.count
    field_aliases = []

    for i in range(num_fields):
        field_alias = field_info.getFieldName(i)
        field_aliases.append(field_alias)

    return field_aliases


def compare_column_names(table_name, csv_first_row, datadict_gdb_alias, csv_path, datadict_csv_gdb_names):
    table_fields = arcpy.ListFields(table_name)
    table_field_aliases = {
        field.aliasName: field.name for field in table_fields}
    csv_to_table_field_map = {}

    # Compara o alias com o nome das colunas do CSV
    logging.info(f"{table_name}:")
    for csv_column in csv_first_row:
        if csv_column in datadict_csv_gdb_names:
            csv_to_table_field_map[csv_column] = datadict_csv_gdb_names[csv_column]
            csv_column = datadict_csv_gdb_names[csv_column]
        if csv_column not in table_field_aliases and csv_column not in datadict_gdb_alias:
            logging.warning(
                f"Nome da Coluna '{csv_column}' não está na tabela;")
        if csv_column in table_field_aliases:
            csv_to_table_field_map[csv_column] = table_field_aliases[csv_column]

    for column in table_field_aliases:
        if column not in csv_to_table_field_map and column not in datadict_gdb_alias:
            arcpy.DeleteField_management(table_name, column)

    csv_data = pd.read_csv(csv_path, encoding='utf-8')
    csv_data.rename(columns=csv_to_table_field_map, inplace=True)
    csv_data.to_csv(csv_path, index=False)
    return csv_to_table_field_map


def append_csv_to_table(csv_path, table_name, datadict_gdb_alias, list_gdb_latlong, datadict_csv_gdb_names):
    try:
        # Lê a primeira coluna do CSV
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_first_row = csv_file.readline().strip().split(',')

        csv_to_table_field_name = compare_column_names(
            table_name, csv_first_row, datadict_gdb_alias, csv_path, datadict_csv_gdb_names)

        if table_name not in list_gdb_latlong:
            # Append do csv nas tabelas
            arcpy.Append_management(csv_path, table_name, 'NO_TEST')

        if table_name == 'VLT':
            csv_data = pd.read_csv(csv_path)
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                csvreader = csv.DictReader(csv_file)
                for row in csvreader:
                    # Extract latitude and longitude values
                    lat_a = float(row["LAT1"].replace(",", "."))
                    lon_a = float(row["LONG1"].replace(",", "."))
                    lat_b = float(row["LAT2"].replace(",", "."))
                    lon_b = float(row["LONG2"].replace(",", "."))

                    # Create a line geometry
                    line = arcpy.Polyline(
                        arcpy.Array([arcpy.Point(lon_a, lat_a),
                                    arcpy.Point(lon_b, lat_b)]),
                    )

                    # Append the line geometry to the list

                    with arcpy.da.InsertCursor(table_name, list(csv_to_table_field_name.values()) + ["SHAPE@"]) as cursor:
                        for csv_row in csv_data.itertuples(index=False):
                            # Prepara o dado para inserção
                            data_for_insertion = [getattr(
                                csv_row, csv_to_table_field_name[field]) for field in csv_to_table_field_name] + [line]
                            cursor.insertRow(data_for_insertion)

        if table_name == 'TLT':
            csv_data = pd.read_csv(csv_path)
            with open(csv_path, 'r', encoding='utf-8') as csv_file:
                csvreader = csv.DictReader(csv_file)
                for row in csvreader:
                    lines = []
                    # Extract latitude and longitude values
                    lat = float(row["LAT"].replace(",", "."))
                    lon = float(row["LONG"].replace(",", "."))

                    # Create a line geometry
                    point = arcpy.Point(lon, lat)

                    with arcpy.da.InsertCursor(table_name, list(csv_to_table_field_name.values()) + ["SHAPE@XY"]) as cursor:
                        for csv_row in csv_data.itertuples(index=False):
                            # Prepara o dado para inserção
                            data_for_insertion = [getattr(
                                csv_row, csv_to_table_field_name[field]) for field in csv_to_table_field_name] + [point]
                            cursor.insertRow(data_for_insertion)
    except Exception as E:
        logging.error(E)
        return E
