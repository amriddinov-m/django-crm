from client.models import ClientType
from order.models import SettingStatus
from payment.models import Cashier, ProjectSetting


def pages(request):
    return {
        'wash_order_statuses': SettingStatus.objects.all(),
        'client_types': ClientType.objects.all(),
        'cashiers': Cashier.objects.order_by('-payment_type'),
        'ps': ProjectSetting.load(),
    }
