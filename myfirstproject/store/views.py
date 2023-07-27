# def admin_panel(request):
#     today = date.today()
    
#     delivered_orders = Order.objects.filter(status='Delivered')
    
#     delivered_orders_by_months = delivered_orders.annotate(
#         delivered_month=ExtractMonth('created_at'),
#         delivered_day=ExtractDay('created_at')
#     ).values('delivered_month', 'delivered_day').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_day', 'delivered_count')
    
#     delivered_orders_month = []
#     delivered_orders_number = []
#     for d in delivered_orders_by_months:
#         if d['delivered_month'] is not None and d['delivered_day'] is not None:
#             month_name = calendar.month_name[d['delivered_month']]
#             day_number = d['delivered_day']
#             delivered_orders_month.append(f"{month_name} {day_number}")
#             delivered_orders_number.append(d['delivered_count'])

#     order_by_months = Order.objects.annotate(
#         month=ExtractMonth('created_at'),
#         day=ExtractDay('created_at')
#     ).values('month', 'day').annotate(count=Count('id')).values('month', 'day', 'count')
    
#     monthNumber = []
#     dayNumber = []
#     totalOrders = []
#     for o in order_by_months:
#         if o['month'] is not None and o['day'] is not None:
#             month_name = calendar.month_name[o['month']]
#             day_number = o['day']
#             monthNumber.append(f"{month_name} {day_number}")
#             dayNumber.append(day_number)
#             totalOrders.append(o['count'])

#     delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
#     delivered_orders_year = []
#     delivered_orders_year_number = []
#     for d in delivered_orders_by_years:
#         if d['delivered_year'] is not None:
#             delivered_orders_year.append(d['delivered_year'])
#             delivered_orders_year_number.append(d['delivered_count'])
    
#     order_by_years = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
#     yearNumber = []
#     totalOrdersYear = []
#     for o in order_by_years:
#         if o['year'] is not None:
#             yearNumber.append(o['year'])
#             totalOrdersYear.append(o['count'])

#     
    
#     context ={
#         'delivered_orders': delivered_orders,
#         'order_by_months': order_by_months,
#         'monthNumber': monthNumber,
#         'dayNumber': dayNumber,
#         'totalOrders': totalOrders,
#         'delivered_orders_number': delivered_orders_number,
#         'delivered_orders_month': delivered_orders_month,
#         'delivered_orders_by_months': delivered_orders_by_months,
#         'today': today,
#         'order_by_years': order_by_years,
#         'yearNumber': yearNumber,
#         'totalOrdersYear': totalOrdersYear,
#         'delivered_orders_year': delivered_orders_year,
#         'delivered_orders_year_number': delivered_orders_year_number,
#         'delivered_orders_by_years': delivered_orders_by_years,
#         
#     }
#     return render(request, 'admin_template/dashboard.html', context)