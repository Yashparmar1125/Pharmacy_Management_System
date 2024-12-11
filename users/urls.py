from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LOGIN, name='login'),
    path('doLOGIN', views.doLOGIN, name='dologin'),
    path('Home/', views.HOME, name='home'),
    path('doLOGOUT/', views.doLOGOUT, name='dologout'),
    path('Dashboard/', views.dashboard, name='dashboard'),

    #Customer
    path('Customer/addCustomerForm/', views.addCustomerForm, name='addcustomerform'),
    path('Customer/addCustomer', views.addCustomer, name='addcustomer'),
    path('Customer/customerList/', views.customerList, name='customerlist'),
    path('Customer/searchCustomer/', views.searchCustomer, name='searchcustomer'),

    #Doctor
    path('Doctor/addDoctor/', views.addDoctor, name='adddoctor'),
    path('Doctor/doctorList/', views.doctorList, name='doctorlist'),
    path('Doctor/removeDoctor/<int:doc_id>', views.removeDoctor, name='removedoctor'),
    path('Doctor/editDoctorForm/<str:doc_id>', views.editDoctorForm, name='editdoctorform'),
    path('Doctor/editDoctor/', views.editDoctor, name='editdoctor'),
    path('Doctor/search/', views.searchDoctor, name='searchdoctor'),

    #Medicine
    path('Medicine/addMedicineForm/', views.addMedicineForm, name='addmedicineform'),
    path('check_med_id/', views.check_med_id, name='check_med_id'),
    path('Medicine/addMedicine/', views.addMedicine, name='addmedicine'),
    path('Medicine/MedicineList/', views.medicineList, name='medicinelist'),
    path('Medicine/placeOrder/<str:medicine_id>', views.placeOrder, name='placeorder'),
    path('Medicine/orderPlaced/', views.orderPlaced, name='orderplaced'),

    #medicine_search/sort
    path('Medicine/search/', views.searchMedicine, name='searchmedicine'),
    path('Medicine/sort/<str:sort>', views.sortMedicine, name='sortmedicine'),

    #Manufacturer
    path('Manufacturer/manufacturerList/', views.manufacturerList, name='manufacturerlist'),
    path('Manufacturer/addManufacturer/', views.addManufacturer, name='addmanufacturer'),
    path('Manufacturer/manufacturerEditForm/<str:id>', views.manufacturerEditForm, name='manufacturereditform'),
    path('Manufacturer/manufacturerEdit/', views.manufacturerEdit, name='editmanufacturer'),
    path('Manufacturer/removeManufacturer/<str:id>', views.removeManufacturer, name='removemanufacturer'),

    #Bills
    path('Bill/viewBill/', views.viewBill, name='viewbill'),
    path('Invoice/<str:cust_id>/', views.invoice, name='invoice'),
    path('Invoice/print/<str:cust_id>', views.printInvoice, name='printinvoice'),

    path('Return/List/', views.returnList, name='returnlist'),
    # path('test-404/', views.raise_404, name='test_404'),
    # path('test-500/', views.raise_500, name='test_500'),

    path('Finance/Income/', views.income, name='income'),
    path('Finance/Expense/', views.expense, name='expense'),
    path('Finance/Income/add_Income/', views.add_income, name='addincome'),
    path('Finance/Income/delete-income/<int:income_id>/', views.delete_income, name='delete_income'),
    path('Finance/Expense/expenses/add/', views.add_expense, name='add_expense'),

    path('Reports/Sales_Report/',views.sales_report, name='sales_report'),
    path('Chart/', views.chart, name='chart'),

]