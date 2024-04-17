# test script that tests output.py's print_to_png function

from output_pdf import print_to_pdf
from output_pdf import myPDFformat
import fpdf


def test_print():
    with open("test_input.txt", "r") as text_file:
        content = [(text_file.read())]

    pdf = myPDFformat('L')
    pdf.alias_nb_pages()

    pdf.set_auto_page_break(auto=True, margin=25)

    pdf.add_page()

    pdf.set_font('arial', '', 13)

    print_to_pdf(pdf, content)

    pdf.output('test_report_2' + '.pdf', 'F')


test_print()
