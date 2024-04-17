# test script that tests if output.py's print_to_png function outputs pngs

from output_pdf import print_to_pdf
from output_pdf import myPDFformat


def main():
    content = ['sample.png']

    pdf = myPDFformat('L')
    pdf.alias_nb_pages()

    pdf.set_auto_page_break(auto=True, margin=25)

    pdf.add_page()

    pdf.set_font('arial', '', 13)

    print_to_pdf(pdf, content)

    pdf.output('test_report_3' + '.pdf', 'F')


main()
