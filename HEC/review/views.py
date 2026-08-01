import datetime
import win32com.client
import pandas
# import pythoncom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from common.models import EmployeeMaster
from review.models import Category, EmpReviewQuesAns, EmployeeReview, EmpReviewRoot
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.template.loader import render_to_string
import pythoncom

from utils.common_utils import clean_date, send_email_notification

pythoncom.CoInitialize()


class EmployeeReviewView(View):
    template_name='review/employee_review.html'

    def get(self, request):
        return render(request,self.template_name)

    def post(self, request, *args, **kwargs):
        employee_id = self.request.POST.get('emp')
        employee_data = EmployeeMaster.objects.filter(EmployeeNumber=employee_id)
        employee_obj = None
        if employee_data.count() == 0:
            messages.error(request, "This employee id does not associate any employee detail.")
            print("error ")
            return redirect("review:employee_review")
        if employee_data.count() >= 1:
            employee_obj = employee_data.first()

        all_category = Category.objects.all()
        data = {
            "employee_obj": employee_obj,
            "all_category": all_category
        }
        return render(request, self.template_name, data)


class EmployeeDetailView(LoginRequiredMixin, View):
    template_name = "review/employee_review.html"

    def get(self,request, *args, **kwargs):
        employee_object_id = self.kwargs['pk']
        employee_data = EmployeeMaster.objects.filter(id=employee_object_id)
        employee_obj = None
        if employee_data.count() >= 1:
            employee_obj = employee_data.first()
        all_category = Category.objects.all()
        data = {
            "employee_obj": employee_obj,
            "all_category": all_category
        }
        return render(request,self.template_name, data)


class EmployeeReviewSubmitView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        employee_id = self.request.POST.get("employee_id")
        employee_obj = EmployeeMaster.objects.get(id=employee_id)

        category_id = self.request.POST.get("category_id")
        category_obj = Category.objects.get(id=category_id)

        category_comment = self.request.POST.get(f"comment-{category_obj.CategoryName}")
        # import code
        # code.interact(local=dict(**globals(), **locals()))
        employee_root_review = EmpReviewRoot.objects.filter(final_status=False, Employee=employee_obj)
        # employee_category_review = employee_obj.employee_review.filter(Category__CategoryName=category_obj.CategoryName)
        # category_question_ans_value = "yes"
        if employee_root_review.exists():
            emp_review_root_obj = employee_root_review.first()
            employee_category_review = emp_review_root_obj.employee_root_category_review.filter(Category__CategoryName=category_obj.CategoryName)
            if employee_category_review.exists():
                existing_employee_category_review_obj = employee_category_review.first()
                existing_employee_category_review_obj.AdditionalComment = category_comment
                existing_employee_category_review_obj.save()
                for cat_question in category_obj.category_question.all():
                    cat_employee_question_ans = existing_employee_category_review_obj.employee_review_ques_ans.filter(Question=cat_question)
                    category_question_ans = self.request.POST.get(f'category_question_ans_checkbox_{cat_question.id}')
                    print(category_question_ans, "category question ansss")
                    remark_cat_que = self.request.POST.get(f'remark_{cat_question.id}', None)
                    if cat_employee_question_ans.exists():
                        cat_employee_question_ans_obj = cat_employee_question_ans.first()
                        cat_employee_question_ans_obj.Review = existing_employee_category_review_obj
                        cat_employee_question_ans_obj.Question = cat_question
                        cat_employee_question_ans_obj.Ans = category_question_ans
                        cat_employee_question_ans_obj.AnsType = cat_question.QuestionType
                        cat_employee_question_ans_obj.remark = remark_cat_que
                        cat_employee_question_ans_obj.save()
                    else:
                        EmpReviewQuesAns.objects.create(Review=existing_employee_category_review_obj,
                                                                    Question=cat_question,
                                                                    Ans=category_question_ans,
                                                                    AnsType=cat_question.QuestionType,
                                                                    remark=remark_cat_que)
            else:
                employee_category_review = EmployeeReview.objects.create(
                    Category=category_obj,
                    employee_root=emp_review_root_obj,
                    AdditionalComment=category_comment
                )
                for cat_question in category_obj.category_question.all():
                    category_question_ans = self.request.POST.get(f'category_question_ans_checkbox_{cat_question.id}')
                    print(category_question_ans, "category question ansss")
                    remark_cat_que = self.request.POST.get(f'remark_{cat_question.id}', None)
                    EmpReviewQuesAns.objects.create(Review=employee_category_review,
                                                    Question=cat_question,
                                                    Ans=category_question_ans,
                                                    AnsType=cat_question.QuestionType,
                                                    remark=remark_cat_que)

            # employee_category_review = employee_category_review.first()
            # for cat_question in category_obj.category_question.all():
            #     category_question_ans = self.request.POST.get(f'category_question_{cat_question.id}', "off")
            #     remark_cat_que = self.request.POST.get(f'remark_{cat_question.id}', None)
            #     if category_question_ans == "on":
            #         category_question_ans_value = "no"
            #         existing_question = employee_category_review.employee_review_ques_ans.filter(Question=cat_question)
            #         if existing_question.exists():
            #             existing_question = existing_question.first()
            #             existing_question.Ans = category_question_ans_value
            #             if remark_cat_que:
            #                 existing_question.remark = remark_cat_que
            #             existing_question.save()
            #         else:
            #             EmpReviewQuesAns.objects.create(Review=employee_category_review,
            #                                             Question=cat_question,
            #                                             Ans=category_question_ans_value,
            #                                             AnsType=cat_question.QuestionType,
            #                                             remark=remark_cat_que)
            #     else:
            #         category_question_ans_value = "yes"
            #         existing_question = employee_category_review.employee_review_ques_ans.filter(
            #             Question=cat_question)
            #         if existing_question.exists():
            #             existing_question = existing_question.first()
            #             existing_question.Ans = category_question_ans_value
            #             if remark_cat_que:
            #                 existing_question.remark = remark_cat_que
            #             existing_question.save()
            #         else:
            #             EmpReviewQuesAns.objects.create(Review=employee_category_review,
            #                                             Question=cat_question,
            #                                             Ans=category_question_ans_value,
            #                                             AnsType=cat_question.QuestionType,
            #                                             remark=remark_cat_que)
            # employee_category_review.AdditionalComment = category_comment
            # employee_category_review.save()
        else:
            emp_review_root_obj = EmpReviewRoot.objects.create(
                Employee=employee_obj
            )
            employee_category_review = EmployeeReview.objects.create(
                Category=category_obj,
                employee_root=emp_review_root_obj,
                AdditionalComment=category_comment
            )
            for cat_question in category_obj.category_question.all():
                category_question_ans = self.request.POST.get(f'category_question_ans_checkbox_{cat_question.id}')
                print(category_question_ans, "category question ansss")
                remark_cat_que = self.request.POST.get(f'remark_{cat_question.id}', None)
                EmpReviewQuesAns.objects.create(Review=employee_category_review,
                                                Question=cat_question,
                                                Ans=category_question_ans,
                                                AnsType=cat_question.QuestionType,
                                                remark=remark_cat_que)
        messages.success(request,"Employee data submit successfully.")
        return redirect(reverse("review:employee_detail", args=[employee_obj.id]))


class EmployeeListView(LoginRequiredMixin, ListView):
    template_name = "review/employee_list.html"
    queryset = EmployeeMaster.objects.all()
    context_object_name = "all_employees"
    paginate_by = 10

    def get_queryset(self):
        query_set = super(EmployeeListView, self).get_queryset()
        search_employee_data = self.request.GET.get('search_data')
        if search_employee_data:
            query_set = EmployeeMaster.objects.filter(Q(EmployeeNumber__icontains=search_employee_data) | Q(EmployeeName__icontains=search_employee_data))
        return query_set


class EmployeeReviewDetailView(LoginRequiredMixin, View):
    template_name = "review/employee_review_detail.html"

    def get(self, request, *args, **kwargs):
        employee_id = self.kwargs['pk']
        employee_obj = EmployeeMaster.objects.get(id=employee_id)
        data = {
            "employee_obj": employee_obj
        }
        return render(request, self.template_name, data)


class EmployeeEditView(LoginRequiredMixin, UpdateView):
    template_name = "review/employee_edit.html"
    model = EmployeeMaster

    def get(self, request, *args, **kwargs):
        employee_object = self.get_object()
        data = {"employee_obj": employee_object}
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        emp_obj = self.get_object()
        emp_name = self.request.POST.get("employee_name")
        position_code = self.request.POST.get("position_code")
        position = self.request.POST.get("position")
        grade_code = self.request.POST.get("grade_code")
        employee_status = self.request.POST.get("employee_status")
        employee_type = self.request.POST.get("employee_type")
        business_unit = self.request.POST.get("business_unit")
        legal_entity = self.request.POST.get("legal_entity")
        dept_oracle_string = self.request.POST.get("dept_oracle_string")
        department_reporting_name = self.request.POST.get("department_reporting_name")
        location = self.request.POST.get("location")
        date_of_birth = self.request.POST.get("date_of_birth")
        age = self.request.POST.get("age")
        gender = self.request.POST.get("gender")
        marital_status = self.request.POST.get("marital_status")
        date_of_join = self.request.POST.get("date_of_join")
        group_date_of_join = self.request.POST.get("group_date_of_join")
        date_of_separation = self.request.POST.get("date_of_separation")
        date_of_retirement = self.request.POST.get("date_of_retirement")
        adani_exp = self.request.POST.get("adani_exp")
        previous_exp = self.request.POST.get("previous_exp")
        total_year_of_exp = self.request.POST.get("total_year_of_exp")
        reporting_manager_id = self.request.POST.get("reporting_manager_id")
        reporting_manager_position = self.request.POST.get("reporting_manager_position")
        reporting_manager_full_name = self.request.POST.get("reporting_manager_full_name")
        hod_emp_id = self.request.POST.get("hod_emp_id")
        hod_full_name = self.request.POST.get("hod_full_name")
        functional_manager_id = self.request.POST.get("functional_manager_id")
        functional_manager_full_name = self.request.POST.get("functional_manager_full_name")
        kra_status = self.request.POST.get("kra_status")
        domicile_state = self.request.POST.get("domicile_state")
        ujr = self.request.POST.get("ujr")
        last_promotion_date = self.request.POST.get("last_promotion_date")
        last_transfer_date = self.request.POST.get("last_transfer_date")
        hod = self.request.POST.get("hod")
        eduction = self.request.POST.get("eduction")
        # total_exp = self.request.POST.get("total_experience")
        compliance_training_status = self.request.POST.get("compliance_training_status")

        # try:
        #     date_of_join_date = datetime.strptime(date_of_join, '%d.%m.%Y').date()
        #     date_of_join_date = date_of_join_date.strftime("%d.%m.%Y")
        # except Exception as e:
        #     print(e, "eee")
        #     date_of_join_date = None
        # if not date_of_join_date:
        #     messages.success(request, "Please enter a valid date formate for Date of Join.")
        #     data = {"employee_obj": emp_obj}
        #     return render(request, self.template_name, data)
        # # print(date_of_join_date.strftime("%d.%m.%Y"), "ddddd")
        emp_obj.EmployeeName = emp_name
        emp_obj.PositionCode = position_code
        emp_obj.Position = position
        emp_obj.GradeCode = grade_code
        emp_obj.EmployeeStatus = employee_status
        emp_obj.EmployeeType = employee_type
        emp_obj.BusinessUnit = business_unit
        emp_obj.LegalEntity = legal_entity
        emp_obj.DepartmentOfOracleString = dept_oracle_string
        emp_obj.DepartmentReportingName = department_reporting_name
        emp_obj.Location = location
        emp_obj.DateOfBirth = clean_date(date_of_birth)
        emp_obj.Age = age or None
        emp_obj.Gender = gender
        emp_obj.MaritalStatus = marital_status
        emp_obj.DateOfJoin = clean_date(date_of_join)
        emp_obj.GroupOfDateOfJoin = clean_date(group_date_of_join)
        emp_obj.DateOfSeparation = clean_date(date_of_separation)
        emp_obj.DateOfRetirement = clean_date(date_of_retirement)
        emp_obj.AdaniExperience = adani_exp or None
        emp_obj.PreviousExperience = previous_exp or None
        emp_obj.TotalYearOfExperience = total_year_of_exp or None
        emp_obj.ReportingMangerID = reporting_manager_id
        emp_obj.ReportingMangerPosition = reporting_manager_position
        emp_obj.ReportingMangerFullName = reporting_manager_full_name
        emp_obj.HODEMPID = hod_emp_id
        emp_obj.HODFullName = hod_full_name
        emp_obj.FunctionalManagerID = functional_manager_id
        emp_obj.FunctionalManagerFullName = functional_manager_full_name
        emp_obj.KRAStatus = kra_status
        emp_obj.DomicileState = domicile_state
        emp_obj.UJR = ujr
        emp_obj.Last_Promotion_Date = clean_date(last_promotion_date)
        emp_obj.Last_Transfer_Date = clean_date(last_transfer_date)
        emp_obj.Hod = hod
        emp_obj.Education = eduction
        emp_obj.Compliance_Training_Status = compliance_training_status
        emp_obj.save()
        messages.success(request,"Employee detail update successfully.")
        data = {"employee_obj": emp_obj}
        return render(request, self.template_name, data)


class EmployeeAddView(LoginRequiredMixin, View):
    template_name = "review/employee_add.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        employee_number = self.request.POST.get("employee_number")
        emp_name = self.request.POST.get("employee_name")
        position_code = self.request.POST.get("position_code")
        position = self.request.POST.get("position")
        grade_code = self.request.POST.get("grade_code")
        employee_status = self.request.POST.get("employee_status")
        employee_type = self.request.POST.get("employee_type")
        business_unit = self.request.POST.get("business_unit")
        legal_entity = self.request.POST.get("legal_entity")
        dept_oracle_string = self.request.POST.get("dept_oracle_string")
        department_reporting_name = self.request.POST.get("department_reporting_name")
        location = self.request.POST.get("location")
        date_of_birth = self.request.POST.get("date_of_birth")
        age = self.request.POST.get("age")
        gender = self.request.POST.get("gender")
        marital_status = self.request.POST.get("marital_status")
        date_of_join = self.request.POST.get("date_of_join")
        group_date_of_join = self.request.POST.get("group_date_of_join")
        date_of_separation = self.request.POST.get("date_of_separation")
        date_of_retirement = self.request.POST.get("date_of_retirement")
        adani_exp = self.request.POST.get("adani_exp")
        previous_exp = self.request.POST.get("previous_exp")
        total_year_of_exp = self.request.POST.get("total_year_of_exp")
        reporting_manager_id = self.request.POST.get("reporting_manager_id")
        reporting_manager_position = self.request.POST.get("reporting_manager_position")
        reporting_manager_full_name = self.request.POST.get("reporting_manager_full_name")
        hod_emp_id = self.request.POST.get("hod_emp_id")
        hod_full_name = self.request.POST.get("hod_full_name")
        functional_manager_id = self.request.POST.get("functional_manager_id")
        functional_manager_full_name = self.request.POST.get("functional_manager_full_name")
        kra_status = self.request.POST.get("kra_status")
        domicile_state = self.request.POST.get("domicile_state")
        ujr = self.request.POST.get("ujr")
        last_promotion_date = self.request.POST.get("last_promotion_date")
        last_transfer_date = self.request.POST.get("last_transfer_date")
        hod = self.request.POST.get("hod")
        eduction = self.request.POST.get("eduction")
        # total_exp = self.request.POST.get("total_experience")
        compliance_training_status = self.request.POST.get("compliance_training_status")

        # try:
        #     date_of_join_date = datetime.strptime(date_of_join, '%d.%m.%Y').date()
        #     date_of_join_date = date_of_join_date.strftime("%d.%m.%Y")
        # except Exception as e:
        #     print(e, "error")
        #     date_of_join_date = None
        # if not date_of_join_date:
        #     messages.success(request, "Please enter a valid date format for Date of Join.")
        #     return render(request, self.template_name)
        if not EmployeeMaster.objects.filter(EmployeeNumber=employee_number).exists():
            EmployeeMaster.objects.create(
                EmployeeNumber=employee_number,
                EmployeeName=emp_name,
                PositionCode=position_code,
                Position=position,
                GradeCode=grade_code,
                EmployeeStatus=employee_status,
                EmployeeType=employee_type,
                BusinessUnit=business_unit,
                LegalEntity=legal_entity,
                DepartmentOfOracleString=dept_oracle_string,
                DepartmentReportingName=department_reporting_name,
                Location=location,
                DateOfBirth=clean_date(date_of_birth),
                Age=age or None,
                Gender=gender,
                MaritalStatus=marital_status,
                DateOfJoin=clean_date(date_of_join),
                GroupOfDateOfJoin=clean_date(group_date_of_join),
                DateOfSeparation=clean_date(date_of_separation),
                DateOfRetirement=clean_date(date_of_retirement),
                AdaniExperience=adani_exp or None,
                PreviousExperience=previous_exp or None,
                TotalYearOfExperience=total_year_of_exp or None,
                ReportingMangerID=reporting_manager_id,
                ReportingMangerPosition=reporting_manager_position,
                ReportingMangerFullName=reporting_manager_full_name,
                HODEMPID=hod_emp_id,
                HODFullName=hod_full_name,
                FunctionalManagerID=functional_manager_id,
                FunctionalManagerFullName=functional_manager_full_name,
                KRAStatus=kra_status,
                DomicileState=domicile_state,
                UJR=ujr,
                Last_Promotion_Date=clean_date(last_promotion_date),
                Last_Transfer_Date=clean_date(last_transfer_date),
                Hod=hod,
                Education=eduction,
                Compliance_Training_Status=compliance_training_status,
            )
            messages.success(request,"Employee detail add successfully.")
        else:
            messages.error(request, "Employee id all ready exists.")
        print()

        return render(request, self.template_name)


class EmployeeFinalSubmit(LoginRequiredMixin, View):
    template_name = "email_templates/review_send_email.html"

    def post(self, request, *args, **kwargs):
        employee_id = self.request.POST.get("employee_id")
        employee_obj = EmployeeMaster.objects.get(id=employee_id)
        employee_all_root_review = employee_obj.employee_review.filter(final_status=False)
        review_obj = employee_all_root_review.last()
        submitted_review_category_count = employee_all_root_review.last().employee_root_category_review.all().count()
        category_store_count = Category.objects.all().count()
        if category_store_count == submitted_review_category_count:
            employee_all_root_review.update(final_status=True,
                                            SubmittedBy=self.request.user,
                                            submitted_date=datetime.now())
            messages.success(request, "Employee data submit successfully.")
            data = {
                "user_name": self.request.user.full_name,
                "employee_name": review_obj.Employee.EmployeeName,
                "employee_review_obj": review_obj
            }
            html_text = render_to_string(self.template_name, data, request)
            # import code
            # code.interact(local=dict(**globals(), **locals()))
            pythoncom.CoInitialize()
            outlook = win32com.client.Dispatch("outlook.application")
            mail = outlook.CreateItem(0)
            mail.To = self.request.user.email
            mail.Subject = f"HR connect with {review_obj.Employee.EmployeeName}"
            mail.HTMLBody = html_text
            mail.Send()

            employee_template_name = self.template_name
            mail_to = self.request.user.email
            subject = f"HR connect with {review_obj.Employee.EmployeeName}"
            # mail_to = "bharadanayan.vijaybhai@adani.com"
            # cc_email = admin_obj.email
            cc_email = "bharadanayan.vijaybhai@adani.com"
            # data = {
            #     'manager_name': manager_user.full_name,
            #     'host_url': PRODUCTION_HOST_URL,
            # }
            send_email_notification(data, employee_template_name, subject, mail_to, cc_email)

        else:
            messages.error(request, "Please fill up the all data.")
        return redirect(reverse("review:employee_detail", args=[employee_obj.id]))


class EmployeeReviewFileSubmit(View):
    template_name = "review/employee_review_file_submit.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        file_obj = self.request.FILES.get("input_file")
        df = pandas.read_excel(file_obj,sheet_name="master_sheet", header=[0], dtype=str)
        header_list = [column_name for column_name in df.columns]

        all_records = df.to_dict('records')
        for raw_record in all_records:
            # print(raw_record, "raw record")
            emp_code = str(raw_record.get("Employee")).replace('nan','')
            print(emp_code, "emp code")

            if emp_code:
                print(emp_code, "emp code, call")
                try:
                    emp_obj = EmployeeMaster.objects.get(EmployeeNumber=emp_code)
                except ObjectDoesNotExist:
                    emp_obj = None
                    print(f"employee does not exists-{emp_code}--exception")
                if emp_obj:
                    new_root_review_create = None
                    # employee root review
                    old_pending_review = EmpReviewRoot.objects.filter(Employee=emp_obj,
                                                                      final_status=False)
                    if old_pending_review.exists():
                        employee_review_root_obj = old_pending_review.last()
                    else:
                        employee_review_root_obj = EmpReviewRoot.objects.create(
                            Employee=emp_obj
                        )
                        new_root_review_create = True

                    for category_obj in Category.objects.all():
                        category_new_create = None

                        category_additional_comment = str(raw_record.get(f"Remarks-{category_obj.id}")).replace('nan', '')

                        # employee category review object
                        employee_category_review = EmployeeReview.objects.filter(employee_root=employee_review_root_obj,
                                                                                 Category=category_obj)
                        if employee_category_review.exists():
                            employee_category_review_obj = employee_category_review.last()
                        else:
                            if category_additional_comment:
                                employee_category_review_obj = EmployeeReview.objects.create(
                                    employee_root=employee_review_root_obj,
                                    Category=category_obj
                                )
                                category_new_create = True
                            else:
                                employee_category_review_obj = None
                                print(f"category remarks missing Employee code-{emp_code} Category name: {category_obj.CategoryName}")
                        if category_additional_comment:
                            employee_category_review_obj.AdditionalComment = category_additional_comment
                            employee_category_review_obj.save()
                        else:
                            employee_category_review_obj = None
                            print(
                                f"category remarks missing for existing categoryEmployee code-{emp_code} Category name: {category_obj.CategoryName}")

                        if employee_category_review_obj:
                            for category_question in category_obj.category_question.all():
                                category_question_ans = str(raw_record.get(f"{category_question.Question}-1")).replace('nan', '')
                                category_question_ans_remark = str(raw_record.get(f"{category_question.Question}-remark")).replace('nan', '')
                                print(category_question.Question, "category question")
                                print(category_question_ans, "ans")
                                print(category_question_ans_remark, "remark")
                                print(" ")
                                if category_question_ans and category_question_ans_remark:
                                    employee_review_que_ans = EmpReviewQuesAns.objects.filter(
                                        Review=employee_category_review_obj,
                                        Question=category_question,
                                    )
                                    if employee_review_que_ans.exists():
                                        employee_review_que_ans_obj = employee_review_que_ans.last()
                                        employee_review_que_ans_obj.Review = employee_category_review_obj
                                        employee_review_que_ans_obj.Question = category_question
                                        employee_review_que_ans_obj.Ans = category_question_ans
                                        employee_review_que_ans_obj.AnsType = category_question.QuestionType
                                        employee_review_que_ans_obj.remark = category_question_ans_remark
                                        employee_review_que_ans_obj.data_is_upload_backend = True
                                        employee_review_que_ans_obj.save()
                                    else:
                                        EmpReviewQuesAns.objects.create(
                                            Review=employee_category_review_obj,
                                            Question=category_question,
                                            Ans=category_question_ans,
                                            AnsType=category_question.QuestionType,
                                            remark=category_question_ans_remark,
                                            data_is_upload_backend=True
                                        )
                                else:
                                    if category_new_create and category_question.id == category_obj.category_question.last().id:
                                        if employee_category_review_obj.employee_review_ques_ans.all().count() == 0:
                                            employee_category_review_obj.delete()
                                            print(f"don't any question found so we delete this record-{emp_code}")

                    if new_root_review_create:
                        if employee_review_root_obj.employee_root_category_review.all().count() == 0:
                            employee_review_root_obj.delete()
                else:
                    print(f"employee does not exists-{emp_code}")
            else:
                pass
        messages.success(request,"file upload success fully.")
        return render(request, self.template_name)


class DemoView(View):
    template_name = "email_templates/review_send_email.html"

    def get(self, request, *args, **kwargs):
        # outlook = win32com.client.dynamic.Dispatch('Outlook.Application')
        pythoncom.CoInitialize()
        outlook = win32com.client.Dispatch('Outlook.Application')
        print(outlook, "outlook")
        review_obj = EmpReviewRoot.objects.last()
        data = {
            "user_name": "nayan",
            "employee_name": review_obj.Employee.EmployeeName,
            "employee_review_obj": review_obj
        }
        # return render(request, self.template_name, data)
        html_text = render_to_string(self.template_name, data, request)
        # import code
        # code.interact(local=dict(**globals(), **locals()))
        mail = outlook.CreateItem(0)
        mail.To = "bharadanayan.vijaybhai@adani.com"
        mail.Subject = f"HR connect with {review_obj.Employee.EmployeeName}"
        mail.HTMLBody = html_text
        mail.Send()
        # outlook = win32com.client.Dispatch('outlook.application')
        # data = {
        #     "user_name": self.request.user,
        #     "employee_review_obj": EmpReviewRoot.objects.last()
        # }
        # html_text = render_to_string(self.template_name, data, request)
        # import code
        # code.interact(local=dict(**globals(), **locals()))
        # mail = outlook.CreateItem(0)
        # mail.To = "vijay.chavda1@adani.com"
        # mail.Subject = "Hr Employee Connect"
        # mail.HTMLBody = html_text
        # mail.Send()
        return HttpResponse("success")


# new design

class ALLEmployeeListView(LoginRequiredMixin, ListView):
    template_name = "employee/employee_list.html"
    queryset = EmployeeMaster.objects.all()
    context_object_name = "all_employees"
    paginate_by = 10

    def get_queryset(self):
        query_set = super(ALLEmployeeListView, self).get_queryset()
        search_employee_data = self.request.GET.get('search_data')
        if search_employee_data:
            query_set = EmployeeMaster.objects.filter(
                Q(EmployeeNumber__icontains=search_employee_data) | Q(EmployeeName__icontains=search_employee_data))
        return query_set


class AddEmployeeView(LoginRequiredMixin, View):
    template_name = 'employee/add_employee.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        employee_number = self.request.POST.get("employee_number")
        emp_name = self.request.POST.get("employee_name")
        position_code = self.request.POST.get("position_code")
        position = self.request.POST.get("position")
        grade_code = self.request.POST.get("grade_code")
        employee_status = self.request.POST.get("employee_status")
        employee_type = self.request.POST.get("employee_type")
        business_unit = self.request.POST.get("business_unit")
        legal_entity = self.request.POST.get("legal_entity")
        dept_oracle_string = self.request.POST.get("dept_oracle_string")
        department_reporting_name = self.request.POST.get("department_reporting_name")
        location = self.request.POST.get("location")
        date_of_birth = self.request.POST.get("date_of_birth")
        age = self.request.POST.get("age")
        gender = self.request.POST.get("gender")
        marital_status = self.request.POST.get("marital_status")
        date_of_join = self.request.POST.get("date_of_join")
        group_date_of_join = self.request.POST.get("group_date_of_join")
        date_of_separation = self.request.POST.get("date_of_separation")
        date_of_retirement = self.request.POST.get("date_of_retirement")
        adani_exp = self.request.POST.get("adani_exp")
        previous_exp = self.request.POST.get("previous_exp")
        total_year_of_exp = self.request.POST.get("total_year_of_exp")
        reporting_manager_id = self.request.POST.get("reporting_manager_id")
        reporting_manager_position = self.request.POST.get("reporting_manager_position")
        reporting_manager_full_name = self.request.POST.get("reporting_manager_full_name")
        hod_emp_id = self.request.POST.get("hod_emp_id")
        hod_full_name = self.request.POST.get("hod_full_name")
        functional_manager_id = self.request.POST.get("functional_manager_id")
        functional_manager_full_name = self.request.POST.get("functional_manager_full_name")
        kra_status = self.request.POST.get("kra_status")
        domicile_state = self.request.POST.get("domicile_state")

        try:
            date_of_join_date = datetime.strptime(date_of_join, '%d.%m.%Y').date()
            date_of_join_date = date_of_join_date.strftime("%d.%m.%Y")
        except Exception as e:
            print(e, "error")
            date_of_join_date = None
        if not date_of_join_date:
            messages.success(request, "Please enter a valid date format for Date of Join.")
            return render(request, self.template_name)
        if not EmployeeMaster.objects.filter(EmployeeNumber=employee_number).exists():
            EmployeeMaster.objects.create(
                EmployeeNumber=employee_number,
                EmployeeName=emp_name,
                PositionCode=position_code,
                Position=position,
                GradeCode=grade_code,
                EmployeeStatus=employee_status,
                EmployeeType=employee_type,
                BusinessUnit=business_unit,
                LegalEntity=legal_entity,
                DepartmentOfOracleString=dept_oracle_string,
                DepartmentReportingName=department_reporting_name,
                Location=location,
                DateOfBirth=date_of_birth,
                Age=age,
                Gender=gender,
                MaritalStatus=marital_status,
                DateOfJoin=date_of_join_date,
                GroupOfDateOfJoin=group_date_of_join,
                DateOfSeparation=date_of_separation,
                DateOfRetirement=date_of_retirement,
                AdaniExperience=adani_exp,
                PreviousExperience=previous_exp,
                TotalYearOfExperience=total_year_of_exp,
                ReportingMangerID=reporting_manager_id,
                ReportingMangerPosition=reporting_manager_position,
                ReportingMangerFullName=reporting_manager_full_name,
                HODEMPID=hod_emp_id,
                HODFullName=hod_full_name,
                FunctionalManagerID=functional_manager_id,
                FunctionalManagerFullName=functional_manager_full_name,
                KRAStatus=kra_status,
                DomicileState=domicile_state
            )
            messages.success(request, "Employee detail add successfully.")
        else:
            messages.error(request, "Employee id all ready exists.")
        return render(request, self.template_name)