# script to take in an input and output it as a pdf

from fpdf import FPDF

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

pdf.sub_header('Part 1: Get Dataset Information')

text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec bibendum imperdiet libero. Etiam tincidunt velit commodo ante volutpat ullamcorper. Aliquam purus enim, feugiat in rutrum ut, sagittis ut est. Pellentesque semper venenatis magna eget sodales. Duis malesuada nibh quis placerat congue. Duis dapibus velit ac cursus finibus. Suspendisse potenti. Pellentesque molestie magna viverra nisi fringilla faucibus. Morbi molestie imperdiet iaculis. Praesent at nibh nisi.Vestibulum efficitur, massa at feugiat scelerisque, urna mauris auctor urna, quis eleifend elit nisi at velit. Cras euismod nunc sit amet augue tincidunt porta. Vestibulum justo lorem, condimentum et lectus eu, accumsan vestibulum ex. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed tellus eu sapien vulputate ultrices. Aliquam rhoncus leo ut lorem accumsan condimentum. Nulla cursus urna ac ante maximus vestibulum. Mauris consequat tellus sagittis ligula rutrum tristique. Integer facilisis sem sed arcu faucibus blandit. Nunc eu est commodo, condimentum lectus eu, ullamcorper felis.'

pdf.set_font('arial', '', 13.0)
pdf.multi_cell(0, 5, text)

pdf.sub_header('Part 2: Privacy policy analysis')


pdf.sub_header('Part 3: Binary files analysis')


pdf.sub_header('Part 4: Results generator')

pdf.output('report.pdf', 'F')

