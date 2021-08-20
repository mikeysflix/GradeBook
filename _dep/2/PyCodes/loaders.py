from pathlib import Path
import numpy as np
from pandas import read_excel

def initialize_raw_data(extension):
    """

    """
    fdir = '/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/'
    fname = 'data'
    fpath = '{}{}{}'.format(fdir, fname, extension)
    extension = Path(fpath).suffix
    if extension in ('.csv', '.txt'):
        raw_data = np.loadtxt(fpath, dtype=str, delimiter=',')
    elif extension in ('.xlsx', '.xls', '.xlsm', '.xlsb', '.xml'):
        df = read_excel(fpath)
        keys = df.keys().tolist()
        values = df.values.tolist()
        raw_data = np.array([keys] + values, dtype=str)
    else:
        raise ValueError("invalid file extension: {}".format(extension))
    # print("\n\n .. RAW DATA:\n\n{}, {}\n".format(raw_data, raw_data.shape))
    print("\n{}\n".format(raw_data.shape))



initialize_raw_data(extension='.csv')
initialize_raw_data(extension='.txt')
initialize_raw_data(extension='.xlsx')







# initialize_raw_data(extension='.pdf')


# import PyPDF2
#     elif extension in ('.pdf', '.PDF'):
#         with open(fpath, 'rb') as f:
#             pdf = PyPDF2.PdfFileReader(f)
#             information = pdf.getDocumentInfo()
#             number_of_pages = pdf.getNumPages()
#
#
#
#         pdf_file = open(fpath, "rb")
#         pdf_reader = PyPDF2.PdfFileReader(pdf_file)
#         raw_data = []
#         for pgn in range(pdf_reader.numPages):
#             pdf_text = pdf_reader.getPage(pgn)
#             raw_data.append(pdf_text.extractText())
#         raw_data = np.array(raw_data)
#     else:
#         ...
#
#
# from io import StringIO
#
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfdocument import PDFDocument
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfpage import PDFPage
# from pdfminer.pdfparser import PDFParser
#
# output_string = StringIO()
# with open('/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.pdf', 'rb') as in_file:
#     parser = PDFParser(in_file)
#     doc = PDFDocument(parser)
#     rsrcmgr = PDFResourceManager()
#     device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     for page in PDFPage.create_pages(doc):
#         interpreter.process_page(page)
#
# print(output_string.getvalue())
#
#
#
#
#
#
# # def extract_information(pdf_path):
# #     with open(pdf_path, 'rb') as f:
# #         pdf = PyPDF2.PdfFileReader(f)
# #         information = pdf.getDocumentInfo()
# #         number_of_pages = pdf.getNumPages()
# #
# #     txt = f"""
# #     Information about {pdf_path}:
# #
# #     Author: {information.author}
# #     Creator: {information.creator}
# #     Producer: {information.producer}
# #     Subject: {information.subject}
# #     Title: {information.title}
# #     Number of pages: {number_of_pages}
# #     """
# #
# #     print(txt)
# #     return information
# #
# # if __name__ == '__main__':
# #     path = '/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.pdf'
# #     extract_information(path)
#
#
#
# # import camelot
# #
# # tables = camelot.read_pdf('/Users/mikeyshmikey/Desktop/Hub/Programming/GradeBook/Data/data.pdf')
# #
# # print("Total tables extracted:", tables.n)
# # print(tables[0].df)
