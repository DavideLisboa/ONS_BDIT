import os
import logging
import arcpy
import var
from esri.authenticate import authenticate
from esri.download_rest import download_file
from esri.status_update import update_status

from update_front.update_token import update_token
import xlsx_to_csv
import append_csv_to_table
import log
import timedate


if __name__ == "__main__":

    token = authenticate(var.PORTAL_URL, var.USERNAME, var.PASSWORD)
    update_token(var.TYPESCRIPT_PATH, token)
    id_to_download = download_file(
        var.PORTAL_URL, var.USERNAME, var.PASSWORD, var.EXCEL_PATH, token)
    if id_to_download:
        datetime = timedate.currentTime()
        log.logs(datetime, var.LOG_PATH)
        logging.info(f"Começando o processamento;")
        logging.info(f"Mudando o status;")
        update_status(var.PORTAL_URL, id_to_download,
                      'em processamento', None, token)
        arcpy.env.workspace = var.GDB_PATH
        # lendo as planilhas e transformando em csv
        filenames = (os.listdir(var.EXCEL_PATH))
        for filename in filenames:
            logging.info(
                f"Transformando o {filename} e suas abas em csvs;")
            csv_files = xlsx_to_csv.xlsx_to_csv(
                f"{var.EXCEL_PATH}\\{filename}", f"{var.CSV_PATH}\\{filename}", filename)
            for csv in csv_files:
                if csv in var.DATADICTCSV_GDB_NAMES:
                    if var.DATADICTCSV_GDB_NAMES.get(csv) in ["", None, " "]:
                        aba = csv.replace(".csv", "")
                        aba = aba.replace(
                            filename.replace(".xlsx", "") + "_", "")
                        logging.warning(
                            f"Aba {aba} não existe nas tabelas;")
                    else:
                        logging.info(
                            f"Adicionando na tabela {var.DATADICTCSV_GDB_NAMES.get(csv)};")
                        error = append_csv_to_table.append_csv_to_table(
                            f"{var.CSV_PATH}\\{csv}", var.DATADICTCSV_GDB_NAMES.get(csv), var.DATADICT_GDB_ALIAS, var.LIST_GDB_LATLONG, var.DATADICT_CSV_GDB_NAMES)
                        if error:
                            update_status(var.PORTAL_URL, id_to_download,
                                          'erro', error, token)
                        else:
                            update_status(var.PORTAL_URL, id_to_download,
                                          'Finalizado', None, token)
