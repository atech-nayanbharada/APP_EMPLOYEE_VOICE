import os
import pandas
import json
from django.core.management.base import BaseCommand, CommandError
from HEC.settings import BASE_DIR
from common.models import EmployeeMaster,DeptMaster
from review.models import Category, CategoryQuestion, EmpReviewRoot, EmployeeReview, EmpReviewQuesAns
from user.models import CustomUser


class Command(BaseCommand):
    """ this command is used for local sqllite database data backup generate in my sql gcp that gcp data through
    power bi dashboard connect """

    def handle(self, *args, **options):
        # user modal backup generate old table data remove
        power_bi_all_custom_user = CustomUser.objects.all().using("power_bi")
        power_bi_all_custom_user.delete()

        # live db data transfer to the power_bi backup db
        all_custom_user = CustomUser.objects.all()
        for custom_user_obj in all_custom_user:
            custom_user_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"User add successfully : {custom_user_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nUser backup successfully."))

        # EmployeeMaster modal backup generate old table data remove
        power_bi_all_employee_master = EmployeeMaster.objects.all().using("power_bi")
        power_bi_all_employee_master.delete()

        # live db data transfer to the power_bi backup db
        all_employee = EmployeeMaster.objects.all()
        for employee_obj in all_employee:
            employee_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Employee add successfully : {employee_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nEmployee backup successfully."))

        # Category modal backup generate old table data remove
        power_bi_all_category = Category.objects.all().using("power_bi")
        power_bi_all_category.delete()

        # live db data transfer to the power_bi backup db
        all_category = Category.objects.all()
        for category_obj in all_category:
            category_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Category add successfully : {category_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nCategory backup successfully."))

        # Category Question modal backup generate old table data remove
        power_bi_all_category_question = CategoryQuestion.objects.all().using("power_bi")
        power_bi_all_category_question.delete()

        # live db data transfer to the power_bi backup db
        all_category_question = CategoryQuestion.objects.all()
        for category_question_obj in all_category_question:
            category_question_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Category question add successfully : {category_question_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nCategory question backup successfully."))

        # emp review root modal backup generate old table data remove
        power_bi_all_emp_review_root = EmpReviewRoot.objects.all().using("power_bi")
        power_bi_all_emp_review_root.delete()

        # live db data transfer to the power_bi backup db
        all_emp_review_root = EmpReviewRoot.objects.all()
        for emp_review_root_obj in all_emp_review_root:
            emp_review_root_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Employee review root add successfully : {emp_review_root_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nEmployee review root  backup successfully."))

        # emp review modal backup generate old table data remove
        power_bi_all_emp_review = EmployeeReview.objects.all().using("power_bi")
        power_bi_all_emp_review.delete()

        # live db data transfer to the power_bi backup db
        all_emp_review = EmployeeReview.objects.all()
        for emp_review_obj in all_emp_review:
            emp_review_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Employee review add successfully : {emp_review_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nEmployee review  backup successfully."))

        # emp review que ans modal backup generate old table data remove
        power_bi_all_emp_review_que_ans = EmpReviewQuesAns.objects.all().using("power_bi")
        power_bi_all_emp_review_que_ans.delete()

        # live db data transfer to the power_bi backup db
        all_emp_review_que_ans = EmpReviewQuesAns.objects.all()
        for emp_review_que_ans_obj in all_emp_review_que_ans:
            emp_review_que_ans_obj.save(using="power_bi")
            self.stdout.write(self.style.SUCCESS(f"Employee review que ans add successfully : {emp_review_que_ans_obj}"))

        self.stdout.write(self.style.SUCCESS(f"\nEmployee review que ans backup successfully."))



