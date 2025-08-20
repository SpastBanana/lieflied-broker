from django.db import models

class Tickets(models.Model):
    invoice_nr = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    ticket_count = models.CharField(max_length=100)
    total_amount = models.CharField(max_length=100)
    date = models.DateField()

    has_payed = models.CharField(max_length=1)
    checked_in = models.CharField(max_length=1)
    email_subscription = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = "Tickets"
    
    def __str__(self):
        return self.invoice_nr
    

class TicketPrice(models.Model):
    ticket_price = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Prijs van één ticket"

    def __str__(self):
        return self.ticket_price
    

class TicketLog(models.Model):
    color_code = models.CharField(max_length=20)
    error_code = models.CharField(max_length=40)
    date = models.DateField()
    log_msg = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Tickets log"

    def __str__(self):
        return self.error_code