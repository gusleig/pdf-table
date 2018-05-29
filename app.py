#import tabula
from tabula import read_pdf

po = {'header': None, 'error_bad_lines': True, 'sep':'; ', 'engine': 'python'}


def read_pdf_file():
    try:
        pd = read_pdf("943703862.pdf", stream=True, lattice=False, output_format="dataframe", encoding='utf-8', java_options=None, pandas_options=po, mutiple_tables=True, pages="all",guess=False)
    except Exception as e:
        print("Error: {}".format(e))
    return pd


df = read_pdf_file()

df.to_csv('otuput.csv', encoding='utf-8')
