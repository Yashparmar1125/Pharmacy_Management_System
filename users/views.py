from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.contrib import messages
from django.views.decorators.http import require_POST
from users.EmailBackend import EmailBackend
from users.models import CustomUser,Doctor,Manufacturer,Medicine,Category,Inventory,Customer,Prescription,Bill,MedDetails,Orders,Incomes,Expenses
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# Create your views here.

from django.shortcuts import render

now = timezone.now()
today = now.date()
one_month_ago = now - timedelta(days=30)
one_week_ago = today - timedelta(days=7)

def custom_csrf_failure(request, reason=""):
    return render(request, 'Error/403.html', {'reason': reason})


def LOGIN(request):
    return render(request, 'login.html')


def doLOGIN(request):
    if request.method == 'POST':
        user=EmailBackend.authenticate(request,username=request.POST.get('email'),password=request.POST.get('password'))
        if user!=None:
            login(request,user)
            user_type=user.user_type
            if user_type=='1':
                return HttpResponsePermanentRedirect('/users/admin/')
                # return redirect('home')

            elif user_type=='2':
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid Email or Password')
                return redirect('login')

        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')


def HOME(request):
    return render(request, 'base.html')

@login_required
def dashboard(request):
    total_sale = Bill.objects.aggregate(total_amount=Sum('total_amount'))['total_amount']
    today_sale = Bill.objects.filter(created_at__date=today).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    last_Month_sale = Bill.objects.filter(created_at__gte=one_month_ago).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0
    customer_count = Customer.objects.count()
    today_expense=Orders.objects.filter(placed_at__date=today).aggregate(order_amount=Sum('order_amount'))['order_amount'] or 0
    today_revenue=float(today_sale)-float(today_sale)*0.10
    total_sales=MedDetails.objects.count()
    products=Medicine.objects.count()
    orders = Orders.objects.all()
    customers = Customer.objects.all()
    # Create a mapping of customer IDs to bill objects
    bill_map = {customer.cust_id: None for customer in customers}
    # Fetch all bills for the relevant customers in one query
    bills = Bill.objects.filter(customer__in=customers)
    # Map bill objects to customer IDs
    for bill in bills:
        bill_map[bill.customer.cust_id] = bill

    context = {'orders': orders, 'total_sale': total_sale, 'today_sale': today_sale, 'last_Month_sale': last_Month_sale,'customer_count': customer_count,'today_revenue':today_revenue,'today_expense':today_expense,'total_sales':total_sales,'products':products,'bill_map':bill_map,'customers':customers}
    return render(request, 'home.html', context)




def doLOGOUT(request):
    logout(request)
    return redirect('login')

@login_required
def addCustomerForm(request):
    medicine = Medicine.objects.all()
    inventories = Inventory.objects.all()  # Fetch all inventories
    doctors = Doctor.objects.all()
    medicines=Medicine.objects.all()

    # Create a mapping from med_id to quantity
    inventory_map = {inventory.medicine.med_id: inventory.quantity for inventory in inventories}
    context = {'medicine': medicine, 'inventory_map': inventory_map, 'doctors': doctors, 'medicines': medicine}
    return render(request, 'addCustomer.html',context)


@login_required
def addDoctor(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        specialization=request.POST.get('specialization')
        doctor=Doctor(name=name,phone=phone,specialization=specialization)
        doctor.save()
        messages.success(request, 'Doctor Added Successfully')
        return redirect('adddoctor')


    return render(request, 'addDoctor.html')

@login_required
def doctorList(request):
    doctors=Doctor.objects.all()
    doctors_count=Doctor.objects.count()
    context={'doctors':doctors,'doctors_count':doctors_count}
    return render(request,'doctorList.html',context)

@login_required
def check_med_id(request):
    med_id = request.GET.get('med_id', None)
    exists = Medicine.objects.filter(med_id=med_id).exists()
    return JsonResponse({'exists': exists})

@login_required
def addMedicineForm(request):
    manufacturer=Manufacturer.objects.all()
    categories = Category.objects.all()
    context={'manufacturer':manufacturer,'categories': categories}

    return render(request, 'addMedicine.html',context)

@login_required
def manufacturerList(request):
    manu_count=Manufacturer.objects.count()
    manufacturers=Manufacturer.objects.all()
    context={'manu_count':manu_count,'manufacturers':manufacturers}
    return render(request, 'manufacturer.html',context)

@login_required
def addManufacturer(request):
    if request.method == 'POST':
        company=request.POST.get('company')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        country=request.POST.get('country')
        city=request.POST.get('city')
        state=request.POST.get('state')
        print(company,email,phone,country,city,state)
        manufacturer=Manufacturer(name=company,phone=phone,email=email,country=country,city=city,state=state)
        manufacturer.save()
        messages.success(request, 'Manufacturer Added Successfully')
        return redirect('manufacturerlist')
    return render(request, 'manufacturer.html')

@login_required
def removeDoctor(request, doc_id):
    doctor=Doctor.objects.get(doc_id=doc_id)
    print("okk")
    doctor.delete()
    messages.success(request, 'Doctor removed successfully')
    return redirect('doctorlist')

@login_required
def editDoctorForm(request,doc_id):
    doctor=Doctor.objects.filter(doc_id=doc_id)
    context = {'doctor':doctor}
    return render(request, 'editDoctor.html', context)

@login_required
def editDoctor(request):
    if request.method == 'POST':
        doc_id = request.POST.get('id')

        # Check if doc_id is provided
        if not doc_id:
            messages.error(request, 'Doctor ID is required.')
            return redirect('doctorlist')

        # Get the doctor object, or return 404 if not found
        doctor = get_object_or_404(Doctor, doc_id=doc_id)

        # Update doctor details
        doctor.name = request.POST.get('name')
        doctor.specialization = request.POST.get('specialization')
        doctor.phone = request.POST.get('phone')
        doctor.save()

        messages.success(request, 'Doctor edited successfully')
        return redirect('doctorlist')

    messages.error(request, 'Invalid request method.')
    return redirect('doctorlist')

@login_required
def manufacturerEditForm(request,id):
    manufacturer=Manufacturer.objects.filter(manufacturer_id=id)
    context = {'manufacturer':manufacturer}
    return render(request, 'manufacturerEdit.html', context)

@login_required
def manufacturerEdit(request):
    if request.method == 'POST':
        manufacturer_id = request.POST.get('id')
        if not manufacturer_id:
            messages.error(request, 'Doctor ID is required.')
            return redirect('manufacturer')
        manufacture=Manufacturer.objects.get(manufacturer_id=manufacturer_id)
        manufacture.name = request.POST.get('company')
        manufacture.email = request.POST.get('email')
        manufacture.phone = request.POST.get('phone')
        manufacture.country = request.POST.get('country')
        manufacture.city = request.POST.get('city')
        manufacture.state = request.POST.get('state')
        manufacture.save()
        messages.success(request, 'Manufacturer edited successfully')
        return redirect('manufacturerlist')

    messages.error(request, 'Invalid request method.')
    return render(request,'manufacturer.html')

@login_required
def removeManufacturer(request, id):
    print('okk')
    manufacturer = Manufacturer.objects.get(manufacturer_id=id) # Use get_object_or_404 for better error handling
    manufacturer.delete()
    messages.success(request, 'Manufacturer removed successfully')
    return redirect('manufacturerlist')

@login_required
def addMedicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        med_id=request.POST.get('med_id')
        gen_name=request.POST.get('gen_name')
        desc=request.POST.get('desc')
        weight=request.POST.get('weight')
        category=request.POST.get('category')
        manufacturer_id=request.POST.get('manufacturer')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        expire_date=request.POST.get('expire_date')
        # Get the Manufacturer instance
        manufacturer = Manufacturer.objects.get(manufacturer_id=manufacturer_id)

        # Create Medicine instance
        medicine = Medicine(
         name=name,
         med_id=med_id,
         generic_name=gen_name,
         description=desc,
         weight=weight,
         category=category,  # Store category as a string
         price=price,
         expire_date=expire_date,
         manufacturer=manufacturer  # Use the Manufacturer instance
         )
        medicine.save()

        # Create Inventory instance
        inventory = Inventory(
                medicine=medicine,
                quantity=stock,
                added_date=timezone.now(),
                expire_date=expire_date,
                updated_date=timezone.now()
            )
        inventory.save()

        messages.success(request, 'Medicine added successfully')
        return redirect('addmedicineform')
    return render(request, 'addMedicine.html')

@login_required
def medicineList(request):
    medicines = Medicine.objects.all()
    inventories = Inventory.objects.all()  # Fetch all inventories

    # Create a mapping from med_id to quantity
    inventory_map = {inventory.medicine.med_id: inventory.quantity for inventory in inventories}
    context = {'medicines':medicines,'inventory_map':inventory_map}
    return render(request, 'medicineList.html',context)

@login_required
def searchMedicine(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        medicines = Medicine.objects.filter(name__icontains=query)
        inventories = Inventory.objects.all()
        inventory_map = {inventory.medicine.med_id: inventory.quantity for inventory in inventories}
        context = {'medicines': medicines, 'inventory_map': inventory_map}
    return render(request,'medicineList.html',context)

@login_required
def sortMedicine(request, sort):
    # Initialize context
    context = {}

    # Get all inventories for use in context
    inventories = Inventory.objects.all()
    inventory_map = {inventory.medicine.med_id: inventory.quantity for inventory in inventories}

    # Sorting logic based on the method
    if sort == 'az':
        medicines = Medicine.objects.all().order_by('name')
    elif sort == 'za':
        medicines = Medicine.objects.all().order_by('-name')
    else:
        medicines = Medicine.objects.all()

    context['medicines'] = medicines
    context['inventory_map'] = inventory_map

    # Render the response with context
    return render(request, 'medicineList.html', context)

@login_required
def searchDoctor(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        doctors = Doctor.objects.filter(name__icontains=query)
        doctors_count = Doctor.objects.count()
        context = {'doctors': doctors, 'doctors_count': doctors_count}
        return render(request, 'doctorList.html', context)

from django.db import transaction  # Import transaction for atomic operations

@require_POST
def addCustomer(request):
    # Get customer information from the form
    name = request.POST.get('name')
    phone_no = request.POST.get('phone_no')
    email = request.POST.get('email')
    address = request.POST.get('address')
    age = request.POST.get('age')
    doc_id = request.POST.get('doc_id')
    gender = request.POST.get('gender')
    status = request.POST.get('status')
    payment_mode=request.POST.get('payment_mode')



    # Validate inputs if necessary

    try:
        # Fetch the Doctor instance
        doctor = Doctor.objects.get(doc_id=doc_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Doctor not found.')
        return redirect('addcustomer')  # Redirect to the form or error page

    # Create a new customer record
    customer = Customer(
        name=name,
        phone_no=phone_no,
        email=email,
        address=address,
        age=age,
        doc_id=doctor,  # Assign the Doctor instance
        gender=gender,
        status=status
    )
    customer.save()

    # Process medicines
    medicines_data = request.POST.getlist('medicines[][name]')
    quantities_data = request.POST.getlist('medicines[][quantity]')

    total_amount = 0  # Initialize total amount for the bill

    # Create a new Prescription instance
    pres = Prescription.objects.create(cust_id=customer, doc_id=doctor)

    # Use transaction to ensure atomicity
    with transaction.atomic():
        # Loop through medicines and quantities to save them
        for medicine_id, quantity in zip(medicines_data, quantities_data):
            if medicine_id and quantity:
                try:
                    medicine = Medicine.objects.get(med_id=medicine_id)
                    quantity = int(quantity)

                    # Check inventory before proceeding
                    inventory_item = Inventory.objects.get(medicine=medicine)
                    if inventory_item.quantity >= quantity:
                        # Create a MedDetails record for each medicine in the prescription
                        med_detail = MedDetails(pres_id=pres, med_id=medicine, quantity=quantity)
                        med_detail.save()

                        # Reduce the quantity in inventory
                        inventory_item.quantity -= quantity
                        inventory_item.save()

                        # Update total amount for the bill
                        total_amount += medicine.price * quantity
                    else:
                        messages.warning(request, f'Not enough stock for {medicine.name}.')
                except ObjectDoesNotExist:
                    messages.error(request, f'Medicine with ID {medicine_id} not found.')
                    continue  # Skip this medicine and continue with the next

        # Create a bill for the customer
        if total_amount > 0:  # Ensure total amount is positive
            Bill.objects.create(customer=customer, total_amount=total_amount,payment_mode=payment_mode)
        else:
            messages.warning(request, 'No medicines were added; bill not generated.')

    messages.success(request, 'Customer and prescription(s) added successfully! Bill generated.')
    bill = Bill.objects.get(customer=customer)
    prescription = Prescription.objects.get(cust_id=customer.cust_id)
    items = MedDetails.objects.filter(pres_id=prescription)
    context = {'customer': customer, 'bill': bill, 'items': items}
    return render(request, 'invoice.html', context)


@login_required
def customerList(request):
    customers = Customer.objects.all()
    context = {'customers':customers}
    customer_count = Customer.objects.count()
    context={'customers':customers,'customer_count':customer_count}
    return render(request,'customerList.html',context)

@login_required
def searchCustomer(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        customers= Customer.objects.filter(name__icontains=query)
        customer_count = Customer.objects.count()
        context = {'customers':customers, 'customer_count':customer_count}
        return render(request, 'customerList.html', context)

@login_required
def viewBill(request):
    customers = Customer.objects.all()

    # Create a mapping of customer IDs to bill objects
    bill_map = {customer.cust_id: None for customer in customers}

    # Fetch all bills for the relevant customers in one query
    bills = Bill.objects.filter(customer__in=customers)

    # Map bill objects to customer IDs
    for bill in bills:
        bill_map[bill.customer.cust_id] = bill

    context={'bill_map':bill_map,'customers':customers}

    return render(request,'billList.html',context)

@login_required
def invoice(request,cust_id):
    customer= Customer.objects.get(cust_id=cust_id)
    bill=Bill.objects.get(customer=customer)
    prescription=Prescription.objects.get(cust_id=cust_id)
    items=MedDetails.objects.filter(pres_id=prescription)
    context={'customer':customer,'bill':bill,'items':items}
    return render(request,'invoice.html',context)

@login_required
def printInvoice(request,cust_id):
    customer = Customer.objects.get(cust_id=cust_id)
    bill = Bill.objects.get(customer=customer)
    prescription = Prescription.objects.get(cust_id=cust_id)
    items = MedDetails.objects.filter(pres_id=prescription)
    context = {'customer': customer, 'bill': bill, 'items': items}
    return render(request, 'invoicePrint.html', context)

@login_required
def placeOrder(request,medicine_id):
    manufacturer=Manufacturer.objects.all()
    context={'manufacturer':manufacturer,'medicine_id':medicine_id}
    return render(request,'placeOrder.html',context)

@login_required
def orderPlaced(request):
    if request.method == 'POST':
        med_id = request.POST.get('med_id')
        quantity = request.POST.get('quantity')
        medicine=Medicine.objects.get(med_id=med_id)
        manufac=Manufacturer.objects.get(manufacturer_id=request.POST.get('manufacturer'))
        order_amount=int(quantity)*medicine.price
        order=Orders(med_id=medicine,quantity=quantity,manufacturer=manufac,order_amount=order_amount)
        order.save()
        messages.success(request, 'Order placed successfully.')
        return redirect('medicinelist')


def returnList(request):
    return render(request,'returnList.html')


from django.http import HttpResponse

# def raise_404(request):
#     raise Http404("This is a test 404 error.")
#
# def raise_500(request):
#     raise Exception("This is a test 500 error.")


def income(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)

    # Total Income (Sales + Incomes)
    total_income = (
        (Bill.objects.aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Today's Income
    today_income = (
        (Bill.objects.filter(created_at__date=today).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__date=today).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Yesterday's Income
    yesterday_income = (
        (Bill.objects.filter(created_at__date=yesterday).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__date=yesterday).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Calculate percentage change for today vs. yesterday
    if yesterday_income > 0:
        today_percentage_change = ((today_income - yesterday_income) / yesterday_income) * 100
    else:
        today_percentage_change = 0  # Or handle as needed

    # Weekly Income
    weekly_income = (
        (Bill.objects.filter(created_at__gte=one_week_ago).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__gte=one_week_ago).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Last Week's Income
    last_week_income = (
        (Bill.objects.filter(created_at__gte=one_week_ago - timedelta(days=7), created_at__lt=one_week_ago).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__gte=one_week_ago - timedelta(days=7), created_at__lt=one_week_ago).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Calculate percentage change for this week vs. last week
    if last_week_income > 0:
        weekly_percentage_change = ((weekly_income - last_week_income) / last_week_income) * 100
    else:
        weekly_percentage_change = 0

    # Monthly Income
    monthly_income = (
        (Bill.objects.filter(created_at__gte=one_month_ago).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__gte=one_month_ago).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Last Month's Income
    last_month_income = (
        (Bill.objects.filter(created_at__gte=one_month_ago - timedelta(days=30), created_at__lt=one_month_ago).aggregate(total_amount=Sum('total_amount'))['total_amount'] or 0) +
        (Incomes.objects.filter(created_at__gte=one_month_ago - timedelta(days=30), created_at__lt=one_month_ago).aggregate(total_amount=Sum('income_amount'))['total_amount'] or 0)
    )

    # Calculate percentage change for this month vs. last month
    if last_month_income > 0:
        monthly_percentage_change = ((monthly_income - last_month_income) / last_month_income) * 100
    else:
        monthly_percentage_change = 0

    # Fetch all incomes
    incomes = Incomes.objects.all()

    context = {
        'total_income': total_income,
        'today_income': today_income,
        'yesterday_income': yesterday_income,
        'today_percentage_change': today_percentage_change,
        'weekly_income': weekly_income,
        'last_week_income': last_week_income,
        'weekly_percentage_change': weekly_percentage_change,
        'monthly_income': monthly_income,
        'last_month_income': last_month_income,
        'monthly_percentage_change': monthly_percentage_change,
        'incomes': incomes,
    }

    return render(request, 'income.html', context)



def expense(request):
    expenses=Expenses.objects.all()
    electricity_total = Expenses.objects.filter(expense_type='Electricity').aggregate(Sum('expense_amount'))[
                            'expense_amount__sum'] or 0
    equipment_total = Expenses.objects.filter(expense_type='Equipment').aggregate(Sum('expense_amount'))[
                          'expense_amount__sum'] or 0
    maintenance_total = Expenses.objects.filter(expense_type='Maintenance').aggregate(Sum('expense_amount'))[
                            'expense_amount__sum'] or 0
    manufacture_total = Expenses.objects.filter(expense_type='Manufacturing').aggregate(Sum('expense_amount'))[
                            'expense_amount__sum'] or 0
    context={'expenses': expenses, 'electricity_total': electricity_total,'equipment_total': equipment_total,'maintenance_total': maintenance_total,'manufacture_total': manufacture_total}
    return render(request,'expense.html',context)

def add_income(request):
    if request.method == 'POST':
        income_type = request.POST.get('income_type')
        description = request.POST.get('description')
        income_amount = request.POST.get('income_amount')

        # Optionally validate data here

        # Create the income record
        Incomes.objects.create(
            income_type=income_type,
            description=description,
            income_amount=income_amount
        )
        messages.success(request, 'Income added successfully.')

        # Redirect to the income list page (update the URL name as necessary)
        return redirect('income')  # Ensure 'income_list' is the correct name of your URL

    return HttpResponse(status=405)


def delete_income(request, income_id):
    if request.method == 'POST':
        income = get_object_or_404(Incomes, income_id=income_id)
        income.delete()
        messages.success(request, 'Income deleted successfully.')
        return redirect('income')  # Ensure this is the correct URL name for your income list

    return HttpResponse(status=405)  # Method Not Allowed if not POST


def add_expense(request):
    if request.method == "POST":
        expense_type = request.POST.get('expense_type')
        description = request.POST.get('description')
        expense_amount = request.POST.get('expense_amount')

        new_expense = Expenses(
            expense_type=expense_type,
            description=description,
            expense_amount=expense_amount
        )
        new_expense.save()
        messages.success(request, 'Expense added successfully.')
        return redirect('expense')


from datetime import datetime, timedelta
def sales_report(request):
    today = datetime.now()
    first_day_current_month = today.replace(day=1)
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    # Total sales for the current month
    total_sales_current_month = Bill.objects.filter(created_at__gte=first_day_current_month).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Total sales for the last month
    total_sales_last_month = Bill.objects.filter(
        created_at__gte=first_day_last_month,
        created_at__lte=last_day_last_month
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Total sales for this week
    sales_this_week = Bill.objects.filter(created_at__gte=today - timedelta(days=7)).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Get all Prescription IDs from Bills in the last month
    prescriptions_last_month = Prescription.objects.filter(cust_id__bill__created_at__gte=first_day_last_month)

    # Most sold medicines in the last month
    most_sold_medicines = MedDetails.objects.filter(
        pres_id__in=prescriptions_last_month
    ).values('med_id__name').annotate(total_sales=Sum('quantity')).order_by('-total_sales')[:5]
    medicines = Medicine.objects.all()  # Get all medicines

    context = {
        'total_sales_current_month': total_sales_current_month,
        'total_sales_last_month': total_sales_last_month,
        'sales_this_week': sales_this_week,
        'most_sold_medicines': most_sold_medicines,
        'medicines': medicines,
    }
    return render(request, 'sales_report.html', context)


def chart(request):
    return render(request, 'chart.html')