import pandas as pd


def saving_data(data_to_save):
    with open("tt_oids_file.txt", 'w') as file:
        file.write(data_to_save)


def format_input_data(row_data):
    x = row_data['OID'].dropna()
    oids = [oid for oid in x]
    ready_oids = [oid[:-2] if oid[-1] == 'X' or oid[-1] == 'Y' else oid for oid in oids]
    ready_oids = [oid[1:] if oid[0] == '.' else oid for oid in ready_oids]
    return ready_oids


def prepare_date(data_lst):
    prepared_date = '\n'.join(line for line in data_lst)
    return prepared_date


if __name__ == '__main__':
    excel_data = pd.read_excel('R&S_2+1_24122020.xlsx', sheet_name='RS 2+1')
    oids_lst = format_input_data(excel_data)
    oids_data = prepare_date(oids_lst)
    saving_data(oids_data)
