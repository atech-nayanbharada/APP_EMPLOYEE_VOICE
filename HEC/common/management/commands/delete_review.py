import os
import pandas
import json
from django.core.management.base import BaseCommand, CommandError
from HEC.settings import BASE_DIR
from common.models import EmployeeMaster,DeptMaster
from review.models import Category, CategoryQuestion, EmpReviewRoot, EmployeeReview, EmpReviewQuesAns
from user.models import CustomUser


class Command(BaseCommand):
    """ Delete root review and sub category and category question ans as well."""

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, help='Enter Employee Root ID')

    def handle(self, *args, **options):
        if options.get("id"):
            root_id = options.get('id')
            emp_review_root_obj = EmpReviewRoot.objects.get(id=root_id)
            for employee_review_category_obj in emp_review_root_obj.employee_root_category_review.all():
                for employee_review_que_ans_obj in employee_review_category_obj.employee_review_ques_ans.all():
                    employee_review_que_ans_obj.delete()
                employee_review_category_obj.delete()
            emp_review_root_obj.delete()
            self.stdout.write(self.style.SUCCESS(f"Review Delete Successfully.  --id"))
        else:
            self.stdout.write(self.style.ERROR(f"Please enter a Employee root id -- --id"))
