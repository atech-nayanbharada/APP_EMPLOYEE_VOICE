from django.contrib import admin
from django.urls import path, include
from review import views
app_name = 'review'

urlpatterns = [
    path('employee-review',views.EmployeeReviewView.as_view(),name="employee_review"),
    path('employee detail/<int:pk>', views.EmployeeDetailView.as_view(), name="employee_detail"),
    path('employee review submit', views.EmployeeReviewSubmitView.as_view(), name="employee_review_submit"),
    path('employee-list/', views.EmployeeListView.as_view(), name="employee_list_view"),
    path('employee-add/', views.EmployeeAddView.as_view(), name="employee_add_view"),
    path('employee-edit/<int:pk>', views.EmployeeEditView.as_view(), name="employee_edit_view"),
    path('review-detail/<int:pk>/', views.EmployeeReviewDetailView.as_view(), name="employee_review_detail_view"),
    path("employee final submit/", views.EmployeeFinalSubmit.as_view(), name="employee_final_submit"),
    path("employee-file", views.EmployeeReviewFileSubmit.as_view(), name="employee_file_submit"),
    path("demo", views.DemoView.as_view(), name="demo"),

    #new design
    path('all_employee_list', views.ALLEmployeeListView.as_view(), name='all_employee_list'),
    path('add_employee', views.AddEmployeeView.as_view(), name='add_employee')

]