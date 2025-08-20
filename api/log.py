from .models import TicketLog
from datetime import datetime

def ticket_log(error, msg):
    log_entry = TicketLog()

    if error.lower() == 'error':
        log_entry.error_code = error
        log_entry.color_code = 'red'
    elif error.lower() == 'warning':
        log_entry.error_code = error
        log_entry.color_code = 'orange'
    elif error.lower() == 'info':
        log_entry.error_code = error
        log_entry.color_code = 'blue'
    elif error.lower() == 'success':
        log_entry.error_code = error
        log_entry.color_code = 'green'
    else:
        log_entry.error_code = 'def'
        log_entry.color_code = 'def'

    log_entry.date = datetime.now()
    log_entry.log_msg = msg

    log_entry.save()