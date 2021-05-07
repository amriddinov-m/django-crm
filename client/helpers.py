from django.urls import reverse

from client.models import Client, Region, ClientType
from order.models import WashOrder, Setting, SettingStatus


def create_client(post_request, user_request):
    full_name = post_request.get('full_name', None)
    address = post_request.get('address', None)
    region = post_request.get('region', None)
    phone = post_request.get('phone', None)
    client_type = post_request.get('client_type', None)
    Client.objects.create(full_name=full_name,
                          phone=phone,
                          address=address,
                          region_id=region,
                          client_type_id=client_type)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-list')),
         'data': ''})


def delete_client(post_request, user_request):
    client_id = post_request.get('client_id', None)
    client = Client.objects.get(id=int(client_id))
    client.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-list')),
         'data': ''})


def create_region(post_request, user_request):
    name = post_request.get('name', None)
    Region.objects.create(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'region-list')),
         'data': ''})


def delete_region(post_request, user_request):
    region_id = post_request.get('region_id', None)
    region = Region.objects.get(id=int(region_id))
    region.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'region-list')),
         'data': ''})


def create_client_type(post_request, user_request):
    name = post_request.get('name', None)
    ClientType.objects.create(name=name)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-type-list')),
         'data': ''})


def delete_client_type(post_request, user_request):
    client_type_id = post_request.get('client_type_id', None)
    client_type = ClientType.objects.get(id=int(client_type_id))
    client_type.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'client-type-list')),
         'data': ''})


def create_wash_order_from_client_list(post_request, user_request):
    client_id = post_request.get('client_id', None)
    status = SettingStatus.objects.get(name='В процессе')
    wash_order = WashOrder.objects.create(client_id=client_id,
                                          user_id=user_request.id,
                                          status_id=status.pk)

    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order.pk}),
         'data': ''})
