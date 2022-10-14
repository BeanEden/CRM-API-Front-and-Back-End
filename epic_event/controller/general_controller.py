"""General views controller (feeds)"""
import datetime
from epic_event.models import Customer, Contract, Event
from operator import attrgetter
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


def date_str_split(date):
    """date reformat for comparison"""
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)


CONTRACT_NOTIFICATIONS = {'payment_due' : ['Payment date is passed.', 'Reshchedule or update status'],
                'event_associated': ['No event associated to this contract','Add a contract now'],
                'status': ['Contract closed before payment date', 'Update contract']

                 }


def check_contract(contract_list):
    """Check contract notification"""
    dict = {}
    for contract in contract_list :
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
        dict[contract] = notification_list
    return dict


def search_customer(query):
    # queryset_company_name = Customer.objects.filter(
    #     company_name__contains=search)
    # queryset_first_name = Customer.objects.filter(first_name__contains = search)
    # queryset_last_name = Customer.objects.filter(last_name__contains = search)
    # queryset_email = Customer.objects.filter(email__contains = search)
    # queryset_phone = Customer.objects.filter(phone__contains = search)
    # queryset_mobile = Customer.objects.filter(mobile__contains = search)
    # queryset_profile = Customer.objects.filter(profile__contains = search)
    # result_list = sorted(
    #     chain(queryset_company_name,
    #           queryset_mobile,
    #           queryset_phone,
    #           queryset_email,
    #           queryset_last_name,
    #           queryset_first_name,
    #           queryset_profile),
    #     key=attrgetter('date_updated'))
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
    # queryset_sales_contact = Contract.objects.filter(
    #     sales_contact__contains=query)
    # queryset_customer_id = Contract.objects.filter(customer_id__contains = query)
    # queryset_name = Contract.objects.filter(name__contains = query)
    # result_list = sorted(
    #     chain(queryset_sales_contact,
    #           queryset_customer_id,
    #           queryset_name),
    #     key=attrgetter('date_updated'))
    result_list = sorted(
        Contract.objects.filter(
            # Q(sales_contact__icontains=query) |
            # Q(customer_id__username__icontains=query) |
            Q(name__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list


def search_event(query):
    # queryset_support_contact = Event.objects.filter(
    #     support_contact__contains=query)
    # queryset_customer_id = Event.objects.filter(customer_id__contains = query)
    # queryset_contract_id = Event.objects.filter(contract_id__contains = query)
    # queryset_event_date = Event.objects.filter(event_date__contains = query)
    # queryset_notes = Event.objects.filter(notes__contains = query)
    # result_list = sorted(
    #     chain(queryset_support_contact,
    #         queryset_customer_id,
    #           queryset_contract_id,
    #           queryset_event_date,
    #           queryset_notes),
    #     key=attrgetter('date_updated'))
    # return result_list
    result_list = sorted(
        Event.objects.filter(
            # Q(support_contact__icontains=query) |
            # Q(customer_id__icontains=query)|
            # Q(contract_id__icontains=query)|
            Q(event_date__icontains=query)|
            Q(notes__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list


def search_user(query):
    # queryset_team = User.objects.filter(
    #     team__contains=search)
    # queryset_first_name = User.objects.filter(first_name__contains = search)
    # queryset_last_name = User.objects.filter(last_name__contains = search)
    # queryset_email = User.objects.filter(email__contains = search)
    # queryset_username = User.objects.filter(username__contains = search)
    # result_list = sorted(
    #     chain(queryset_team,
    #           queryset_email,
    #           queryset_last_name,
    #           queryset_first_name,
    #           queryset_username),
    #     key=attrgetter('date_updated'))
    result_list = sorted(
        User.objects.filter(
            Q(team__icontains=query) |
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)|
            Q(email__icontains=query)|
            Q(username__icontains=query)),
        key=attrgetter('date_updated'))
    return result_list