from tabula import read_pdf
import re
import pandas as pd

po = {'header': None, 'error_bad_lines': True, 'sep': '; ', 'engine': 'python'}


def read_pdf_file():
    try:
        pd = read_pdf("943703862.pdf", stream=True, output_format="dataframe", area=(39.07, 27.13, 819.94, 552.27),
                      encoding='utf-8', java_options=None, pandas_options=po, mutiple_tables=False, pages="all",guess=False)
        # json = read_pdf("943703862.pdf", stream=True, lattice=False, output_format="json", encoding='latin-1', java_options=None,pandas_options=po, mutiple_tables=True, pages="all",guess=False)
    except Exception as e:
        print("Error: {}".format(e))

    # print(json)

    return pd


df = read_pdf_file()

# export csv
df.to_csv('output.csv',  sep=',', encoding='utf-8')


cdr_obj = []

anumber = ""

for index, row in df.iterrows():
    rowstr = row[0]
    # get A number

    anumberstr = rowstr.replace(' ', '')

    match_anumber = re.findall(r'\(\d{2}\)\D*\d{5}\D*[^,]*', str(anumberstr),re.MULTILINE)

    if match_anumber:
        anumber = ' '.join(match_anumber)

    # get index
    # match_index = re.search(r'^[0-9]{10}([,]*?)', rowstr)
    # find 10 digits betweens non digits
    match_index = re.findall(r'(?<!\d)(\d{10})(?!\d)\D*',rowstr)

    if match_index:
        indx = match_index[0]
        if len(match_index)>1:
            if int(match_index[0])!=int(match_index[1])-1:
                match_index = [match_index[0]]


    else:
        indx = ""

    match_date = re.findall(r'\d{2}/\d{2}/\d{4}', rowstr)

    if match_date:
        date = match_date[0]
    else:
        date = ""

    match_hour = re.findall(r'(?:\d{1,2}:?)[0-5]\d:[0-5]\d', rowstr)

    if match_hour:
        hour = match_hour[0]
        if len(match_index) == 1:
            match_hour = [match_hour[0]]

    else:
        hour = ""

    match_dur = re.findall(r'\,(\d{2}:\d{2}:\d{2})', rowstr)

    if match_dur:
        dur = match_dur[0]
    else:
        match_dur = re.findall(r'([0-9]+kb)', rowstr)


    match_numb = re.findall(r'\D(\d{8,11}),', rowstr)

    if match_numb:
        num_b = match_numb[0]
    else:
        num_b = ""

    match_desc_serv1 = re.findall(r'.*?,\s*(.*?),.*', rowstr)

    if match_desc_serv1:
        desc_serv1 = match_desc_serv1[0]
    else:
        desc_serv1 = ""

    # look value between double quotes
    match_val = re.findall(r'\"([0-9]+\D[1]*[0-9]+)\"', rowstr)

    if match_val:
        for i, val in enumerate(match_val):
            match_val[i] = re.sub('"', '', val)
    else:
        val = ""

    # date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()

    if match_index and match_date  and match_hour and match_numb:
        # generate CDR
        print("generates CDR OK")
        for i, val in enumerate(match_index):
            try:
                cdr_obj.append({'index': str(match_index[i]), 'num_a': anumber , 'date': str(match_date[i]), 'hour': str(match_hour[i].replace(' ', '')),
                'duration': str(match_dur[i]), 'num_b': str(match_numb[i]), 'desc_serv1': str(match_desc_serv1[i]), 'val': str(match_val[i])})
            except IndexError as e:
                print(e)

    print(row[0])

df2 = pd.DataFrame(cdr_obj)


df2.to_csv('output_clean.csv',  sep=',', encoding='utf-8')

