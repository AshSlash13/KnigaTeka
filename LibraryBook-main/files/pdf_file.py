import os

from fpdf import FPDF
from domain_models.book import Book

class PdfFile:
    OUTPUT_FOLDER = "library_output"

    @staticmethod
    def _next_file_name():
        files = os.listdir(PdfFile.OUTPUT_FOLDER)
        max_file = 0
        for file in files:
            current_file_number = int(file.title().upper().replace("OUTPUT_(", "").replace(").PDF", ""))
            max_file = max(max_file, current_file_number)
        max_file = max_file + 1
        return 'Output_(%s).pdf' % max_file

    @staticmethod
    def save(results):
        if not os.path.exists(PdfFile.OUTPUT_FOLDER):
            os.mkdir(PdfFile.OUTPUT_FOLDER)

        pdf = FPDF('P', 'mm', 'A4')
        filename = PdfFile.OUTPUT_FOLDER + "/" + PdfFile._next_file_name()

        pdf.add_font("Calibri", "", "calibri.ttf", uni=True)
        pdf.set_font('Calibri', '', 14)
        pdf.add_page()
        print('<Книготека>:')
        pdf.write(8, 'Книготека')
        pdf.ln(8)
        for result in results:
            (book_id, book) = result
            formatted_book = "%s: %s, %s (%s)" % (book_id, book.author, book.title, book.year)
            print(formatted_book)
            pdf.write(8, formatted_book)
            pdf.ln(8)
        pdf.output(filename, 'F')
        pdf.close()
        os.system("start %s" % filename)
        print(r"Файл открыт '%s'" % filename)

    @staticmethod
    def save_one(result):
        PdfFile.save([result])




