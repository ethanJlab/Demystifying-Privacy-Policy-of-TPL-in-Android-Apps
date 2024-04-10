# script to take in an input and output it as a pdf

from fpdf import FPDF
from script_runner import output_list

title = 'ATP Checker Analysis Report'

class myPDFformat(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 20)

        # calculate title width and position
        titleWidth = self.get_string_width(title) + 6 # padding
        docWidth = self.w
        self.set_x((docWidth - titleWidth) / 2)

        self.cell(titleWidth, 10, title, border=False, ln=True, align='C')
        self.ln()

    def sub_header(self, subtitle):
        self.set_font('helvetica', 'U', 15)

        # calculate title width and position
        titleWidth = self.get_string_width(subtitle) + 6 # padding
        docWidth = self.w
        # self.set_x((docWidth - titleWidth) / 2)

        self.cell(120, 10, subtitle, border=False, ln=True)
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


pdf = myPDFformat()
pdf.alias_nb_pages()

pdf.set_auto_page_break(auto=True, margin=15)

pdf.add_page()


# pdf.multi_cell(0, 5, text)

# pdf.sub_header("Part 1: Get Dataset Information")
# pdf.set_font('arial', '', 13.0)

for item in output_list:
    if "Part " in item:
        pdf.cell(0, 5, '', ln=True)
        pdf.sub_header(item)
        pdf.set_font('arial', '', 13)
        continue
    pdf.multi_cell(0, 5, item)


pdf.output('report.pdf', 'F')



# array of strings (variables)
# paths start with './'
