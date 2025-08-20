from log import ticket_log
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate
import os, fitz, smtplib

IMAP_SERVER = 'imap.bhosted.nl'
IMAP_PORT = 993
SMTP_SERVER = 'smtp.bhosted.nl'
SMTP_PORT = 465

AUTOMATIONS_ACCOUNT = 'automations@liefenlied.nl'
AUTOMATIONS_PASSWORD = 'hQA5Zy4FxX'
FOLDER_INBOX = 'Inbox'
FOLDER_SEND = 'Inbox.Send'
FOLDER_DB = 'Inbox.DB'
FOLDER_ERROR = 'Inbox.Error'

KAARTEN_ACCOUNT = 'kaarten@liefenlied.nl'
KAARTEN_PASSWORD = 'fX7Za2zTdD'

DOWNLOAD_FOLDER = 'ticket-requests'


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = f'{BASE_DIR}'.replace('BROKER', 'LOG')
BROKER_ATTACHMENTS = f'{BASE_DIR}'.replace('BROKER', 'Attachments')
HOME_DIR = f'{BASE_DIR}'.replace('/BROKER', '')
INVOICE_DIR = f'{BASE_DIR}'.replace('BROKER', 'PDF')

TICKET_PRICE_INT = 12.5
TICKET_PRICE_STR_COMMA = '12,50'
TICKET_PRICE_STR_DOT = '12.50'

def broker(input_first_name, input_last_name, input_email, input_ticket_count):
    filepath = ''

    # Create new invoice number
    try:
        invoice_numbers = []

        with open(f'{BASE_DIR}/invoices.txt', 'r') as f:
            for line in f:
                invoice_numbers.append(line)

        last_number = invoice_numbers[-1]
        last_number = last_number.split('-')
        last_number = int(last_number[1])
        new_number = f'2025-{"{:04d}".format(last_number + 1)}'
    except Exception as e:
        ticket_log('ERROR', 'Could not create new invoice number:')
        ticket_log('ERROR', str(e))
        email_success = False
        pass

    # Create data for invoice
    try:
        with open(filepath, 'r') as f:
            temp = []

            for line in f:
                context = line.replace('"', '').replace('\n', '').split(',')
                temp.append(context)
            
            submittion = temp[1]

            data = {
                '#NAME' : f'{submittion[1]} {submittion[2]}',
                '#COUNT' : f'{submittion[3]}',
                '#AMOUNT' : f'{str("{:.2f}".format(float(submittion[3])*TICKET_PRICE_INT)).replace('.', ',')}',
                '#TOTALAMOUNT' : f'{str("{:.2f}".format(float(submittion[3])*TICKET_PRICE_INT)).replace('.', ',')}',
                '#FANUMB' : f'{new_number}',
                '#DATE' : f'{datetime.now().strftime("%d-%m-%Y")}',
            }

            create_invoice_pdf(f'{HOME_DIR}/factuur.pdf', f'{INVOICE_DIR}/{new_number}.pdf', data)
    except Exception as e:
        email_success = False
        ticket_log('ERROR', 'Could not create invoice:')
        ticket_log('ERROR', str(e))
        pass

    # Send invoice to custommer
    try:
        with open(filepath, 'r') as f:
            temp = []

            for line in f:
                context = line.replace('"', '').replace('\n', '').split(',')
                temp.append(context)
            
            submittion = temp[1]

            data = {
                '#NAME' : f'{submittion[1]} {submittion[2]}',
                '#COUNT' : f'{submittion[3]}',
                '#AMOUNT' : f'{str("{:.2f}".format(float(submittion[3])*TICKET_PRICE_INT)).replace('.', ',')}',
                '#TOTALAMOUNT' : f'{str("{:.2f}".format(float(submittion[3])*TICKET_PRICE_INT)).replace('.', ',')}',
                '#FANUMB' : f'{new_number}',
                '#DATE' : f'{datetime.now().strftime("%d-%m-%Y")}',
            }

            msg = f'''Beste {submittion[1]} {submittion[2]},

Wij zijn ontzettend blij dat u naar ons concert wilt komen! Bij deze sturen wij u de factuur om de betaling van uw kaarten te kunnen voldoen.

LET OP: Het email adres waarop u deze mail ontvang is tevens uw toegang tot het concert.

Wij zien u graag op het concert!

Met vriendelijke groet,
Stichting Lief & Lied                         
            '''

            send_invoice(str(submittion[4]), f'Betreffende bestelde kaarten | Factuur: {new_number}', msg, [f'{INVOICE_DIR}/{new_number}.pdf'])

    except Exception as e:
        ticket_log('ERROR', 'Could not send the invoice to the custommer:')
        ticket_log('ERROR', str(e))
        email_success = False


def create_invoice_pdf(input_path, output_path, word_replacements):
    """
    Advanced word replacement preserving all original formatting
    """
    doc = fitz.open(input_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Get all text blocks with formatting information
        blocks = page.get_text("dict")
        
        # Process each word replacement
        for old_word, new_word in word_replacements.items():
            # Search for all instances of the old word
            text_instances = page.search_for(old_word)
            
            for inst in text_instances:
                # Find the text block that contains this instance
                text_info = None
                for block in blocks["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                span_rect = fitz.Rect(span["bbox"])
                                if span_rect.intersects(inst):
                                    text_info = span
                                    break
                            if text_info:
                                break
                    if text_info:
                        break
                
                if text_info:
                    # Extract original formatting
                    font = text_info["font"]
                    fontsize = text_info["size"]
                    flags = text_info["flags"]  # bold, italic, etc.
                    color = text_info.get("color", 0)  # text color
                    
                    # Cover the old text with a white rectangle
                    page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))

                    x = inst[0]  # X coordinate stays the same
                    y = inst[1] + 9  # Y coordinate moves down
                    
                    # Insert new text with preserved formatting
                    page.insert_text(
                        (x,y),  # position
                        new_word,
                        fontsize=fontsize
                    )
    
    # Save the modified PDF
    doc.save(output_path)
    doc.close()
    ticket_log('success', f'Saved {output_path}')


def send_invoice(send_to, subject, text, files=None):
    msg = MIMEMultipart()
    msg['From'] = KAARTEN_ACCOUNT
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=os.path.basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
        msg.attach(part)


    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(KAARTEN_ACCOUNT, KAARTEN_PASSWORD)
        server.sendmail(KAARTEN_ACCOUNT, send_to, msg.as_string())
        server.close()