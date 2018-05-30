#import tabula
from tabula import read_pdf
import re
import pandas as pd

po = {'header': None, 'error_bad_lines': True, 'sep': '; ', 'engine': 'python'}


def read_pdf_file():
    try:
        pd = read_pdf("943703862.pdf", stream=True, lattice=False, output_format="dataframe", encoding='latin-1', java_options=None,pandas_options=po, mutiple_tables=True, pages="all",guess=False)
        # json = read_pdf("943703862.pdf", stream=True, lattice=False, output_format="json", encoding='latin-1', java_options=None,pandas_options=po, mutiple_tables=True, pages="all",guess=False)
    except Exception as e:
        print("Error: {}".format(e))

    # print(json)

    return pd


df = read_pdf_file()

cdr_obj = []

anumber = ""

for index, row in df.iterrows():
    rowstr = row[0]
    # get A number

    anumberstr = rowstr.replace(' ', '')
    match = re.search(r'\((\d{2})\)\D*(\d{5})\D*([^,]*)', anumberstr)

    if match:
        anumber = match.group()

    # get index

    match_index = re.search(r'^[0-9]{10}([,]*?)', rowstr)

    if match_index:
        indx = match_index.group()
    else:
        indx = ""

    match_date = re.search(r'(\d{2})/(\d{2})/(\d{4})', rowstr)

    if match_date:
        date = match_date.group()
    else:
        date = ""

    match_hour = re.search(r'\d{2}:\d{2}:\d{2}', rowstr)

    if match_hour:
        hour = match_hour.group()
    else:
        hour = ""

    match_dur = re.search(r'\,(\d{2}:\d{2}:\d{2})', rowstr)

    if match_dur:
        dur = match_dur.group(1)
    else:
        dur = ""

    match_numb = re.search(r'\D(\d{8,11}),', rowstr)

    if match_numb:
        num_b = match_numb.group(1)
    else:
        num_b = ""

    match_desc_serv1 = re.search(r'.*?,\s*(.*?),.*', rowstr)

    if match_desc_serv1:
        desc_serv1 = match_desc_serv1.group(1)
    else:
        desc_serv1 = ""

    # look value between double quotes
    match_val = re.search(r'''(["'])(?:(?=(\\?))\2.)*?\1''', rowstr)

    if match_val:
        val = match_val.group()
        val = re.sub('"', '', val)

    else:
        val = ""

    # date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()

    if match_index and match_date and match_dur and match_hour and match_numb:
        # generate CDR
        print("generates CDR OK")
        cdr_obj.append({'index': indx, 'num_a': anumber, 'date': date, 'hour': hour,
                        'duration': dur, 'num_b': num_b, 'desc_serv1': desc_serv1, 'val': val})

    print(row[0])

df2 = pd.DataFrame(cdr_obj)


df2.to_csv('output_clean.csv',  sep=',', encoding='utf-8')
df.to_csv('output.csv',  sep=',', encoding='utf-8')
