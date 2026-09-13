"""
This is the unique ticket code generator
"""
# import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'it_support.settings')
# django.setup()
import random
from .models import Ticket

def ticket_generation():
    random__num = random.randint(11111,99999)
    print(random__num)
    return random__num
    
def generate_unique_ticket_code():
    # ticket = Ticket.objects.get(
    #     ticket_code = ticket_generation()
    # )
    code = True
    
    while code == True:
        new_ticket_code = ticket_generation()
        code = Ticket.objects.filter(ticket_code=new_ticket_code).exists()
    print(new_ticket_code)
    return new_ticket_code