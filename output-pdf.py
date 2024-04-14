# script to take in an input and output it as a pdf

from fpdf import FPDF
import fitz
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
    pdf.set_font('arial', '', 13)

    for item in p2_list:
        pdf.multi_cell(0, 5, str(item))

    pdf.multi_cell(0, 5, '============================================')

    pdf.sub_header("Part 3: Binary files analysis (no output generated)")
    pdf.set_font('arial', '', 13)

    pdf.multi_cell(0, 5, '============================================')

    pdf.sub_header("Part 4: Results generator")
    pdf.set_font('arial', '', 13)

    def pdf_to_png(pdf_path, png_path):
        # Open the PDF
        pdf_document = fitz.open(pdf_path)

        # Iterate over each page
        for page_number in range(len(pdf_document)):
            # Get the page
            page = pdf_document[page_number]

            # Render the page as an image (high-quality)
            pixmap = page.get_pixmap(alpha=False)

            # Save the image as PNG
            pixmap.save(f"{png_path}.png")

        # Close the PDF
        pdf_document.close()

    for item in p4_list:
        item_as_string = str(item)
        item_length = len(item_as_string)
        # check file type
        if item_as_string[item_length-4:item_length] == ".png":
            pdf.add_page()
            pdf.multi_cell(0, 5, "Running generate_FCG_evaluation")
            pdf.image(item, pdf.get_x(), pdf.get_y(), 190)
            continue
        elif item_as_string[item_length-4:item_length] == ".pdf":
            pdf.add_page()
            pdf.multi_cell(0, 5, "Running draw_fig_5")
            pdf_to_png(item_as_string, "Fig5")
            to_png = "Fig5.png"
            pdf.image(to_png, pdf.get_x(), pdf.get_y(), 190)
            continue
        pdf.multi_cell(0, 5, item_as_string)

pdf.output('report.pdf', 'F')



# array of strings (variables)
# paths start with './'
