from django.contrib import admin
from review.models import Category, CategoryQuestion,EmpReviewQuesAns,EmployeeReview,EmpReviewRoot
# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryQuestion)
admin.site.register(EmpReviewQuesAns)
admin.site.register(EmployeeReview)
admin.site.register(EmpReviewRoot)