import datetime
from django import template
from django.utils import timezone

def date_str_split(date):
    """date reformat for comparison"""
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)


MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

register = template.Library()

CONTRACT_NOTIFICATIONS = {
    'payment_due': ['Payment date is passed.',
                    'Reschedule or update status'],
    'event_associated': ['No event associated to this contract',
                         'Add an event'],
    'status': ['Contract closed before payment date',
               'Update contract']
                 }

@register.filter
def model_type(value):
    return type(value).__name__

@register.filter
def rating_value(rating):
    return int(rating)

@register.filter
def get_posted_at_display(posted_at):
    seconds_ago = (timezone.now() - posted_at).total_seconds()
    if seconds_ago <= HOUR:
        return f'Publié il y a {int(seconds_ago // MINUTE)} minutes.'
    elif seconds_ago <= DAY:
        return f'Publié il y a {int(seconds_ago // HOUR)} heures.'
    return f'Publié le {posted_at.strftime("%d %b %y à %Hh%M")}'


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context['user']:
        return 'Vous avez'
    return user.username +" a "


@register.simple_tag(takes_context=True)
def get_poster_display_review(context, user):
    if user == context['user']:
        return 'Vous avez'
    return str(user) + " a "

@register.simple_tag(takes_context=True)
def get_query(context, request):
    query = ''
    if request.method == "GET":
        query = request.GET.get('search')
        if query == None:
            query = 'All'
    return query.capitalize()



@register.simple_tag(takes_context=True)
def check_user(context, user):
    if user == context['user']:
        return True
    return user.username



def check_contract(contract):
    scheduled_date = date_str_split(str(contract.payment_due))
    now = datetime.datetime.now()
    now = date_str_split(now)
    notification_dict = {}
    # notification_list = []
    if scheduled_date < now and contract.status:
        notification_dict['payment_due'] = CONTRACT_NOTIFICATIONS['payment_due']
        # notification_list.append(CONTRACT_NOTIFICATIONS['payment_due'])
    if contract.event_associated == 'uncomplete':
        notification_dict['event_associated'] = CONTRACT_NOTIFICATIONS[
            'event_associated']
        # notification_list.append(CONTRACT_NOTIFICATIONS['event_associated'])
    if not contract.status and scheduled_date > now:
        notification_dict['status'] = CONTRACT_NOTIFICATIONS[
            'status']
        # notification_list.append(CONTRACT_NOTIFICATIONS['status'])
    return notification_dict


@register.filter
def table_contract_detail(contract):
    notification_dict = check_contract(contract)
    table = []
    for key, value in notification_dict.items():
        line = [key, value[0], value[1]]
        table.append(line)
    return table