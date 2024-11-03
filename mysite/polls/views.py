from django.shortcuts import render
from .models import Investment, Expense

def finances(request):

    investments = Investment.objects.all()
    expenses = Expense.objects.all()
    total_revenue = round(sum(investment.projected_revenue() for investment in investments), 1)
    total_loss = round(sum(float(expense.projected_loss()) for expense in expenses), 1)
    total_profit = round(total_revenue - total_loss, 1)

    return render(request, 'polls/finances.html', {'investments': investments,'expenses': expenses,'total_revenue': total_revenue, 'total_loss': total_loss,'total_profit': total_profit,})