from django.http import HttpResponse
from django.template import loader, Context
from django.urls import reverse

from order.models import Team, WashOrder, WashOrderItem
from payment.helpers import payment_income


def create_team(post_request, user_request):
    worker_name = post_request.get('worker_name', None)
    phone = post_request.get('phone', None)
    car_numb = post_request.get('car_numb', None)
    status = post_request.get('status', None)
    Team.objects.create(worker_name=worker_name,
                        phone=phone,
                        car_numb=car_numb,
                        status=status)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'team-list')),
         'data': ''})


def delete_team(post_request, user_request):
    team_id = post_request.get('team_id', None)
    team = Team.objects.get(id=int(team_id))
    team.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'team-list')),
         'data': ''})


def create_wash_order(post_request, user_request):
    team_id = post_request.get('team', None)
    client_id = post_request.get('client', None)
    status_id = post_request.get('status', None)
    end_time = post_request.get('end_time', None)
    WashOrder.objects.create(team_id=int(team_id),
                             client_id=int(client_id),
                             status_id=status_id,
                             user=user_request,
                             end_time=end_time)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-list')),
         'data': ''})


def delete_wash_order(post_request, user_request):
    wash_order_id = post_request.get('wash_order_id', None)
    wash_order = WashOrder.objects.get(id=int(wash_order_id))
    wash_order.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-list')),
         'data': ''})


def create_wash_order_item(post_request, user_request):
    x_size = post_request.get('x_size', None)
    y_size = post_request.get('y_size', None)
    area = post_request.get('area', None)
    summa = post_request.get('summa', None)
    wash_order_id = post_request.get('wash_order_pk', None)
    WashOrderItem.objects.create(wash_order_id=wash_order_id,
                                 x_size=x_size,
                                 y_size=y_size,
                                 area=area,
                                 summa=summa)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_id}),
         'data': ''})


def delete_wash_order_item(post_request, user_request):
    wash_order_item_id = post_request.get('wash_order_item_id', None)
    wash_order_id = post_request.get('wash_order_id', None)
    wash_order_item = WashOrderItem.objects.get(id=int(wash_order_item_id))
    wash_order_item.delete()
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_id}),
         'data': ''})


# def search_order_from_anywhere(post_request, user_request):
#     wash_orders = post_request.get('wash_order_name', '')
#     template = loader.get_template('wash-order-list.html')
#     context = Context({'wash_orders': wash_orders, })
#     return HttpResponse(template.render(context))


def update_wash_order_item(post_request, user_request):
    wash_order_item_id = post_request.get('wash_order_item_pk', None)
    wash_order_pk = post_request.get('wash_order_pk', None)
    x_size = post_request.get('x_size', None)
    y_size = post_request.get('y_size', None)
    area = post_request.get('area', None)
    summa = post_request.get('summa', None).replace(',', '')
    WashOrderItem.objects.filter(pk=wash_order_item_id).update(x_size=float(x_size),
                                                               y_size=float(y_size),
                                                               area=float(area),
                                                               summa=int(summa))
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order_pk}),
         'data': ''})


def update_team_and_status(post_request, user_request):
    pk = post_request.get('wash_order_pk', None)
    wash_order = WashOrder.objects.get(pk=pk)
    team_value = post_request.get('team_value', None)
    status_value = post_request.get('status_value', None)
    WashOrder.objects.filter(pk=pk).update(team_id=team_value if team_value is not '' else wash_order.team_id,
                                           status_id=status_value)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': pk}),
         'data': ''})


def order_payment(post_request, user_request):
    wash_order_pk = post_request.get('wash_order_pk', None)
    wash_order = WashOrder.objects.get(pk=wash_order_pk)
    value_outlay_amount = post_request.get('amount', 0)
    value_outlay_comment = post_request.get('comment', '')
    value_outlay_amount_method = post_request.get('payment_method', '')
    payment_income(value_outlay_amount, value_outlay_amount_method, value_outlay_comment, user_request,
                   True, 1, wash_order.pk, order_pk=wash_order_pk)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'wash-order-detail'), kwargs={'pk': wash_order.pk}),
         'data': ''})
