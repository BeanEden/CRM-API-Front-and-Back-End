import datetime
def date_str_split(date):
    date = str(date)
    days = date[:10].replace("-", "")
    hours = date[11:16].replace(":", "")
    date = days+hours
    return str(date)

class GlobalFeed(LoginRequiredMixin, APIView, PaginatedViewMixin):
    """Class view used to generate a paginated list of all tickets and reviews
    ordered chronologically (soonest first)
    """
    template_name = 'home.html'

    def get(self, request, **kwargs):
        """
        argument: GET request
        return: url + page_object (= paginated posts)
        """
        customers = Customer.objects.all()
        contracts = Contract.objects.all()
        events = Event.objects.all()
        posts_paged = self.paginate_view(
            request, sorted(chain(customers, contracts, events),
                            key=lambda x: x.date_updated, reverse=True))
        return render(request, self.template_name,
                      context={'page_obj': posts_paged})


CONTRACT_NOTIFICATIONS = {'payment_due' : ['Payment date is passed.', 'Reshchedule or update status'],
                'event_associated': ['No event associated to this contract','Add a contract now'],
                'status': ['Contract closed before payment date', 'Update contract']

                 }


def check_contract(contract_list) :
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

def check_event_associated(contract)

