from django.db.models import Sum, Subquery, OuterRef, Count, IntegerField, F, Q
from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from client.models import Client
from order.models import WashOrder, WashOrderItem, Team
from payment.models import PaymentLog


class ReportIncomePaymentsView(TemplateView):
    template_name = 'report_income_payments.html'

    def get_context_data(self, **kwargs):
        context = super(ReportIncomePaymentsView, self).get_context_data(**kwargs)
        startdate = self.request.GET.get('startdate', '')
        enddate = self.request.GET.get('enddate', '')
        context['startdate'] = startdate
        context['enddate'] = enddate
        if startdate and enddate:
            payments = PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"]) \
                .select_related('user').order_by('-created')
            wash_order_totals = WashOrder.objects \
                .filter(created_at__range=[startdate + ' 00:00', enddate + ' 23:59']) \
                .aggregate(count=Count('pk', distinct='pk'),
                           items_count=Count('wash_order_item'),
                           total_area=Sum('wash_order_item__area'),
                           total_summa=Sum('wash_order_item__summa'), )
            context['wash_order_totals'] = wash_order_totals
            context['report_payments'] = payments
            context['sum_amount'] = payments.aggregate(payment_cash_total_amount=Sum('amount',
                                                                                     filter=Q(payment_method='cash')),
                                                       payment_card_total_amount=Sum('amount',
                                                                                     filter=Q(payment_method='card')))
            context['report_teams'] = Team.objects.prefetch_related('wash_order') \
                .annotate(count_wash_order=Count('wash_order',
                                                 filter=Q(wash_order__created_at__range=
                                                          [startdate + " 00:00", enddate + " 23:59"])),
                          count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk'),
                                                                 wash_order__created_at__range=
                                                                 [startdate + " 00:00", enddate + " 23:59"]) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(count=Count('pk')) \
                                                         .values('count')),
                          area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                        .filter(wash_order__team_id=OuterRef('pk'),
                                                                wash_order__created_at__range=
                                                                [startdate + " 00:00", enddate + " 23:59"]) \
                                                        .values('wash_order__team_id') \
                                                        .annotate(area=Sum('area')) \
                                                        .values('area')),
                          summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk'),
                                                                 wash_order__created_at__range=
                                                                 [startdate + " 00:00", enddate + " 23:59"]) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(summa=Sum('summa')) \
                                                         .values('summa'))) \
                .values('id',
                        'worker_name',
                        'count_wash_order',
                        'count_wash_order_item',
                        'area_wash_order_item',
                        'summa_wash_order_item')
        else:
            payments = PaymentLog.objects.filter(outcat=1).order_by('-created').select_related('user')
            context['sum_amount'] = payments.aggregate(Sum('amount'))
            context['report_teams'] = Team.objects.prefetch_related('wash_order') \
                .annotate(count_wash_order=Count('wash_order'),
                          count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk')) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(count=Count('pk')) \
                                                         .values('count')),
                          area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                        .filter(wash_order__team_id=OuterRef('pk')) \
                                                        .values('wash_order__team_id') \
                                                        .annotate(area=Sum('area')) \
                                                        .values('area')),
                          summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
                                                         .filter(wash_order__team_id=OuterRef('pk')) \
                                                         .values('wash_order__team_id') \
                                                         .annotate(summa=Sum('summa')) \
                                                         .values('summa'))) \
                .values('id',
                        'worker_name',
                        'count_wash_order',
                        'count_wash_order_item',
                        'area_wash_order_item',
                        'summa_wash_order_item')
            context['report_payments'] = PaymentLog.objects.select_related('user') \
                .order_by('-created')
        return context

    # def get_queryset(self):
    #     startdate = self.request.GET.get('startdate', '')
    #     enddate = self.request.GET.get('enddate', '')
    #     if startdate and enddate:
    #         # return PaymentLog.objects.filter(created__range=[startdate + " 00:00", enddate + " 23:59"], outcat=1) \
    #         #     .select_related('user')\
    #         #     .annotate(team=Subquery(Team.objects.filter(id=OuterRef('outlay_child')).values('worker_name')))\
    #         #     .order_by('-created')
    #         # wash_order_item = WashOrderItem.objects.select_related('wash_order')\
    #         #     .filter(wash_order_id=OuterRef('pk')) \
    #         #     .values('wash_order') \
    #         #     .annotate(count=Count('pk')) \
    #         #     .values('count')
    #         # print(wash_order_item)
    #         return Team.objects.prefetch_related('wash_order') \
    #             .annotate(count_wash_order=Count('wash_order',
    #                                              filter=Q(wash_order__created_at__range=
    #                                                       [startdate + " 00:00", enddate + " 23:59"])),
    #                       count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                      .filter(wash_order__team_id=OuterRef('pk'),
    #                                                              wash_order__created_at__range=
    #                                                              [startdate + " 00:00", enddate + " 23:59"]) \
    #                                                      .values('wash_order__team_id') \
    #                                                      .annotate(count=Count('pk')) \
    #                                                      .values('count')),
    #                       area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                     .filter(wash_order__team_id=OuterRef('pk'),
    #                                                             wash_order__created_at__range=
    #                                                             [startdate + " 00:00", enddate + " 23:59"]) \
    #                                                     .values('wash_order__team_id') \
    #                                                     .annotate(area=Sum('area')) \
    #                                                     .values('area')),
    #                       summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                      .filter(wash_order__team_id=OuterRef('pk'),
    #                                                              wash_order__created_at__range=
    #                                                              [startdate + " 00:00", enddate + " 23:59"]) \
    #                                                      .values('wash_order__team_id') \
    #                                                      .annotate(summa=Sum('summa')) \
    #                                                      .values('summa'))) \
    #             .values('id',
    #                     'worker_name',
    #                     'count_wash_order',
    #                     'count_wash_order_item',
    #                     'area_wash_order_item',
    #                     'summa_wash_order_item')
    #     else:
    #         return Team.objects.prefetch_related('wash_order') \
    #             .annotate(count_wash_order=Count('wash_order'),
    #                       count_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                      .filter(wash_order__team_id=OuterRef('pk')) \
    #                                                      .values('wash_order__team_id') \
    #                                                      .annotate(count=Count('pk')) \
    #                                                      .values('count')),
    #                       area_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                     .filter(wash_order__team_id=OuterRef('pk')) \
    #                                                     .values('wash_order__team_id') \
    #                                                     .annotate(area=Sum('area')) \
    #                                                     .values('area')),
    #                       summa_wash_order_item=Subquery(WashOrderItem.objects.select_related('wash_order__team') \
    #                                                      .filter(wash_order__team_id=OuterRef('pk')) \
    #                                                      .values('wash_order__team_id') \
    #                                                      .annotate(summa=Sum('summa')) \
    #                                                      .values('summa'))) \
    #             .values('id',
    #                     'worker_name',
    #                     'count_wash_order',
    #                     'count_wash_order_item',
    #                     'area_wash_order_item',
    #                     'summa_wash_order_item')
    #     #     return PaymentLog.objects.filter(outcat=1).select_related('user')\
    #     #         .annotate(team=Subquery(Team.objects.filter(id=OuterRef('outlay_child')).values('worker_name')),
    #     #                   count_wash_order=Subquery(WashOrder.objects.filter(team_id=OuterRef('outlay_child'))
    #     #                                             .values('team')
    #     #                                             .annotate(count=Count('pk'))
    #     #                                             .values('count')))\
    #     #         .order_by('-created')
