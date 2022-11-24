import csv
from fpdf import FPDF
from datetime import datetime
from Database import createConnection
from Exceptions import NoDataFoundException


def import_from_csv():
    """Import words from csv file."""
    #trying this out
    with open ('words.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(row)
    pass



def export_to_csv():
    """Export words to csv file."""

    conn= createConnection()
    c=conn.cursor()
    c.execute("SELECT * FROM words")
    words = c.fetchall()
    if len(words) <= 0:
            raise NoDataFoundException
    with open('VocabularyBuilder.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ "word", "datetime", "tag", "mastered", "learning", "favorite"])
        writer.writerows(words)



def export_to_pdf():
    """Export words to pdf file."""
    class PDF(FPDF):
        def header(self):
            #self.image('logo.png', 10, 8, 33)
            self.set_font('helvetica', 'B', 15)
            # Move to the right
            self.set_title("Vocabulary Builder")
            
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
    c.execute("SELECT * FROM words")
    rows = c.fetchall()
    i=1
    if len(rows) <= 0:
            raise NoDataFoundException
    pdf.cell(15,8, txt="SrNo",border=True, align='L')
    pdf.cell(20,8, txt="Word",border=True, align='L')
    pdf.cell(60,8, txt="Date Time",border=True, align='L')
    pdf.cell(20,8, txt="Tag",border=True, align='L')
    pdf.cell(20,8, txt="Mastered",border=True, align='L')
    pdf.cell(20,8, txt="Learning",border=True, align='L')
    pdf.cell(20,8, txt="Favorite",border=True, align='L')
    pdf.ln()    
    for row in rows:
            pdf.cell(15,8, txt=str(i),border=True, align='L')
            pdf.cell(20,8, txt=str(row[0]),border=True, align='L')
            pdf.cell(60,8, txt=str(row[1]),border=True, align='L')
            pdf.cell(20,8, txt=str(row[2]),border=True, align='L')
            pdf.cell(20,8, txt=str(row[3]),border=True, align='L')
            pdf.cell(20,8, txt=str(row[4]),border=True, align='L')
            pdf.cell(20,8, txt=str(row[5]),border=True, align='L')
            pdf.ln()
            i=i+1
    
    pdf.output("VocabularyBuilder.pdf")