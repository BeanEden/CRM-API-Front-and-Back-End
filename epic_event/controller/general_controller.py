"""General views controller (feeds)"""
import datetime
from itertools import chain
from operator import attrgetter
from django.contrib.auth import get_user_model
from django.db.models import Q
from epic_event.models import Customer, Contract, Event

User = get_user_model()


def date_str_split(date):
    """date reformat for comparison"""
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)


CONTRACT_NOTIFICATIONS = {
    'payment_due': ['Payment date is passed.',
                    'Reschedule or update status'],
    'event_associated': ['No event associated to this contract',
                         'Add a contract now'],
    'status': ['Contract closed before payment date',
               'Update contract']
                 }




def get_last_posts_selected(query):
    posts = ""
    if query == None:
        customers = Customer.objects.all()
        contracts = Contract.objects.all()
        events = Event.objects.all()
        posts = chain(customers, contracts, events)
    elif query == 'customers':
        posts = Customer.objects.all()
    elif query == 'contracts':
        posts = Contract.objects.all()
    elif query == 'events':
        posts = Event.objects.all()
    return posts





def check_contract(contract_list):
    """Check contract notification"""
    contract_dict = {}
    for contract in contract_list:
        scheduled_date = date_str_split(str(contract.payment_due))
        now = datetime.datetime.now()
        now = date_str_split(now)
        notification_list = []
        if scheduled_date < now and contract.status:
            notification_list.append(CONTRACT_NOTIFICATIONS['payment_due'])
        if contract.event_associated == 'uncomplete':
            notification_list.append(CONTRACT_NOTIFICATIONS['payment_due'])
        if not contract.status and scheduled_date > now:
            notification_list.append(CONTRACT_NOTIFICATIONS['payment_due'])
        contract_dict[contract] = notification_list
    return contract_dict


def search_customer(query):
    """Customer search"""
    result_list = sorted(
        Customer.objects.filter(
            Q(company_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(mobile__icontains=query) |
            Q(profile__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list


def search_contract(query):
    """Contract search"""
    result_list = sorted(
        Contract.objects.filter(
            Q(name__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list


def search_event(query):
    """Event search"""
    result_list = sorted(
        Event.objects.filter(
            Q(event_date__icontains=query) |
            Q(notes__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list


def search_user(query):
    """User search"""
    result_list = sorted(
        User.objects.filter(
            Q(team__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(username__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list
