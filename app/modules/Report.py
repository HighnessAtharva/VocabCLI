from fpdf import FPDF
from datetime import datetime
from Database import createConnection

# have added standard pdf structure
class PDF(FPDF):
        def header(self):
            #self.image('logo.png', 10, 8, 33)
            self.set_font('helvetica', 'B', 15)
            # Move to the right
            self.set_title("Vocabulary Builder Report")
            
            self.cell(55)
            self.cell(80, 10, 'Vocabulary Builder', border=1, align='C')
            self.ln(20)

        # Page footer
        def footer(self):
            #self.set_creation_date = datetime.now()
            self.set_y(-15)
            self.set_font('helvetica', 'I', 10)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
            #self.cell(0, 10, self.creation_date, 0, 0, 'L')
    
pdf=PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("helvetica","", size=12)
conn= createConnection()
c=conn.cursor()

def learning_rate():
    pass

def generate_text_report():

    pdf.output("TextReport.pdf")

def generate_graph_report():
    
    pdf.output("GraphReport.pdf")