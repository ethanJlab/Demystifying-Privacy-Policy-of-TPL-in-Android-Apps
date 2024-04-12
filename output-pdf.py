# script to take in an input and output it as a pdf

from fpdf import FPDF
from script_runner import prelude_list
from script_runner import p1_list
from script_runner import p2_list
from script_runner import p3_list
from script_runner import p4_list


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


TEST = False

pdf = myPDFformat('L')
pdf.alias_nb_pages()

pdf.set_auto_page_break(auto=True, margin=25)

pdf.add_page()


# pdf.multi_cell(0, 5, text)

# pdf.sub_header("Part 1: Get Dataset Information")
# pdf.set_font('arial', '', 13.0)


# prelude header here?

pdf.set_font('arial', '', 13.0)

for item in prelude_list:
    pdf.multi_cell(0, 5, str(item))

pdf.multi_cell(0, 5, '============================================')

pdf.sub_header("Part 1: Get Dataset Information")
pdf.set_font('arial', '', 13.0)

for item in p1_list:
    pdf.multi_cell(0, 5, str(item))

if not TEST:
    pdf.multi_cell(0, 5, '============================================')

    pdf.sub_header("Part 2: Privacy policy analysis (no further output generated)")
    pdf.set_font('arial', '', 13.0)

    for item in p2_list:
        pdf.multi_cell(0, 5, str(item))

    pdf.multi_cell(0, 5, '============================================')

    pdf.sub_header("Part 3: Binary files analysis (no output generated)")
    pdf.set_font('arial', '', 13.0)

    pdf.multi_cell(0, 5, '============================================')

    pdf.sub_header("Part 4: Results generator")
    pdf.set_font('arial', '', 13.0)

    for item in p4_list:
        item_as_string = str(item)
        item_length = len(item_as_string)
        if item_as_string[item_length-4:item_length] == ".png":
            pdf.image(item, 15, 13, 30)
        pdf.multi_cell(0, 5, str(item))

pdf.output('report.pdf', 'F')



# array of strings (variables)
# paths start with './'
