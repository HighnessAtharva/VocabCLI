import csv
from fpdf import FPDF
from datetime import datetime
from Database import createConnection
from Exceptions import NoDataFoundException
from datetime import datetime
from rich import print
from rich.panel import Panel

def export_to_csv():
    """Export words to csv file."""
    conn= createConnection()
    c=conn.cursor()
    try:
        c.execute("SELECT * FROM words")
        words = c.fetchall()
        if len(words) <= 0:
            raise NoDataFoundException
        with open('VocabularyBuilder.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ "word", "datetime", "tag", "mastered", "learning", "favorite"])
            writer.writerows(words)
        print(Panel(f"[bold green]EXPORTED[/bold green] [bold blue]{len(words)}[/bold blue] words to [bold blue]VocabularyBuilder.csv[/bold blue]file 📁"))
    except NoDataFoundException as e:
        print(e)
        
        
def import_from_csv(): 
    """Import words from csv file."""
    conn= createConnection()
    c=conn.cursor()
    
    # count of words added to database from the csv file
    added_words=0 
    
    # words that already exists in database (counter will be incremented everytime SQL throws an error about datetime column UNIQUE constraint violation)
    word_already_exists=0 
    
    try:
        with open ('VocabularyBuilder.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader) # skip header
            sql="INSERT INTO words (word, datetime, tag, mastered, learning, favorite) VALUES (?,?,?,?,?,?)"
            for row in reader:
                try:
                    # add a checker to see if the word already exists in the database with the same timestamp
                    c.execute(sql, row)
                    conn.commit()
                    added_words += c.rowcount
                except Exception as e:
                    word_already_exists+=1
    except FileNotFoundError:
        print(Panel("[bold red]FILE NOT FOUND[/bold red] ❌. Make sure you have a file named [bold red]VocabularyBuilder.csv[/bold red] in the same directory as the executable file. 📂"))
    
    finally:
        if word_already_exists>0:
            if word_already_exists == 1:
                print(Panel(f"[bold red]SKIPPED[/bold red] [bold blue]{word_already_exists}[/bold blue] DUPLICATE WORD WITH THE SAME TIMESTAMP ⏩"))
            else:
                print(Panel(f"[bold red]SKIPPED[/bold red] [bold blue]{word_already_exists}[/bold blue] DUPLICATE WORDS WITH THE SAME TIMESTAMP ⏩"))
        
        
        if added_words == 1:
            print(Panel(f"[bold green]IMPORTED[/bold green] [bold blue]{added_words}[/bold blue] WORD ✅"))
        else:
            print(Panel(f"[bold green]IMPORTED[/bold green] [bold blue]{added_words}[/bold blue] WORDS ✅"))
        


class PDF(FPDF):
    def header(self):
        #self.image('logo.png', 10, 8, 33)
        
        self.set_font('helvetica', 'B', 15)
        
        self.set_title("Vocabulary Builder")
        self.cell(55)
        self.cell(80, 10, 'Vocabulary Builder', border=1, align='C')
        self.ln(20)
    
    
    def footer(self):
        """Page footer."""
        self.set_y(-15)
        self.set_font('helvetica', 'I', 10)
        
        # Page number
        self.cell(0, 10, f'Page {str(self.page_no())}', 0, 0, 'C')
        


def export_to_pdf():    # sourcery skip: extract-method
    """Export words to pdf file."""
    try:
        pdf=PDF('P', 'mm', 'A4')
        pdf.set_fill_color(r=152, g=251, b=152)
        pdf.set_auto_page_break(auto=True, margin=5)
        pdf.add_page()
        pdf.set_font("Arial","B", 12)
        conn= createConnection()
        c=conn.cursor()
        c.execute("SELECT * FROM words")
        rows = c.fetchall()
        if len(rows) <= 0:
            raise NoDataFoundException
        pdf.cell(10,8, txt="#",border=True, align='L', fill=True)
        pdf.cell(40,8, txt="Word",border=True, align='L', fill=True)
        pdf.cell(40,8, txt="Lookup Date",border=True, align='L', fill=True)
        pdf.cell(30,8, txt="Tag",border=True, align='L', fill=True)
        pdf.cell(20,8, txt="Mastered",border=True, align='L', fill=True)
        pdf.cell(20,8, txt="Learning ",border=True, align='L', fill=True)
        pdf.cell(20,8, txt="Favorite",border=True, align='L', fill=True)
        pdf.ln()

        #reset font
        pdf.set_font("Courier","",10)
        for sr_no, row in enumerate(rows, start=1):

            pdf.cell(10,8, txt=str(sr_no),border=True, align='L') # Sr No.
            pdf.cell(40,8, txt=str(row[0]),border=True, align='L') # Word

            date=datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            date=date.strftime('%b %d \'%y | %H:%M')
            pdf.cell(40,8, txt=str(date),border=True, align='L') # Lookup Date

            tag = row[2] if row[2] != None else ""
            pdf.cell(30,8, txt=str(tag),border=True, align='L') # Tag

            mastered= "X" if row[3] == 1 else ""
            pdf.cell(20,8, txt=mastered ,border=True, align='C') # Mastered

            learning= "X" if row[4] == 1 else ""
            pdf.cell(20,8, txt=learning,border=True, align='C') # Learning

            favorite= "X" if row[5] == 1 else ""
            pdf.cell(20,8, txt=favorite,border=True, align='C')  # Favorite
            pdf.ln()
        pdf.output(f"VocabularyWords[{datetime.now().strftime('%d_%b_%Y')}].pdf")
        print(Panel(f"[bold green]EXPORTED[/bold green] [bold blue]{len(rows)}[/bold blue] WORDS TO PDF ✅"))
    
    except NoDataFoundException as e:
        print(e)
