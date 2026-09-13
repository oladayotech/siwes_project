"""
This is the unique ticket code generator
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_support.settings')
django.setup()
import random
from user import models

def ticket_gen():
    random__num = random.randint(11111,99999)
    print(random__num)
    return random__num
    
def ticket_code_exist():
    # ticket = Ticket.objects.get(
    #     ticket_code = ticket_gen()
    # )
    ticket_code = None
    
    while ticket_code == None:
        new_ticket_code = ticket_gen()
        ticket_code = models.Ticket.objects.get(
            ticket_code = new_ticket_code
        )
    print(ticket_code)
    return ticket_code