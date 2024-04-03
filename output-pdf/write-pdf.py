# script to take in an input and output it as a pdf

from fpdf import FPDF

title = 'Any title I want'

class myPDFformat(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)

        # calculate title width and position
        titleWidth = self.get_string_width(title) + 6 # padding
        docWidth = self.w
        self.set_x((docWidth - titleWidth) / 2)

        self.cell(titleWidth, 10, title, border=True, ln=True, align='C')
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


pdf = myPDFformat()
pdf.alias_nb_pages()

pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font('times', 'B', 13.0)

pdf.add_page()

for i in range(40):
    pdf.cell(120, 10, 'Hello', ln=True, border=True)

pdf.output('test.pdf', 'F')

