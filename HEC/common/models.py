from django.db import models
from django_extensions.db.models import TimeStampedModel,ActivatorModel
import math

# Create your models here.
class DeptMaster(TimeStampedModel,ActivatorModel):
    DeptName=models.CharField(max_length=100)
    CoeLeadEmpid=models.CharField(max_length=100,null=True)
    GPOLeadEmpid = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.DeptName


class EmployeeMaster(models.Model):
    EmployeeNumber=models.CharField(max_length=500,null=True , unique=True)
    EmployeeName=models.CharField(max_length=500,null=True)
    PositionCode = models.CharField(max_length=255, null=True)
    Position=models.CharField(max_length=255,null=True)
    GradeCode = models.CharField(max_length=255, null=True)
    EmployeeStatus = models.CharField(max_length=500, null=True)
    EmployeeType = models.CharField(max_length=500, null=True)
    BusinessUnit = models.CharField(max_length=255, null=True)
    LegalEntity = models.CharField(max_length=255, null=True)
    DepartmentOfOracleString = models.CharField(max_length=500, null=True)
    DepartmentReportingName = models.CharField(max_length=255, null=True)
    Location = models.CharField(max_length=255, null=True)
    DateOfBirth=models.DateField(null=True, blank=True)
    Age = models.CharField(null=True,max_length=500)
    Gender = models.CharField(max_length=255, null=True)
    MaritalStatus = models.CharField(max_length=500, null=True)
    DateOfJoin = models.DateField(null=True, blank=True)
    GroupOfDateOfJoin = models.DateField(null=True, blank=True)
    DateOfSeparation = models.DateField(null=True, blank=True)
    DateOfRetirement = models.DateField(null=True, blank=True)
    AdaniExperience = models.CharField(max_length=500, null=True)
    PreviousExperience = models.CharField(max_length=500, null=True)
    TotalYearOfExperience = models.CharField(max_length=500, null=True)
    ReportingMangerID = models.CharField(max_length=500, null=True)
    ReportingMangerPosition = models.CharField(max_length=500, null=True)
    ReportingMangerFullName = models.CharField(max_length=500, null=True)
    HODEMPID = models.CharField(max_length=500, null=True)
    HODFullName = models.CharField(max_length=500, null=True)
    FunctionalManagerID = models.CharField(max_length=500, null=True)
    FunctionalManagerFullName = models.CharField(max_length=500, null=True)
    KRAStatus = models.CharField(max_length=500, null=True)
    DomicileState = models.CharField(max_length=500, null=True)
    UJR = models.CharField(max_length=500, null=True, blank=True)
    Last_Promotion_Date = models.DateField(null=True, blank=True)
    Last_Transfer_Date = models.DateField(null=True, blank=True)
    Hod = models.CharField(max_length=500, null=True, blank=True)
    Education = models.CharField(max_length=500, null=True, blank=True)
    # Total_Experience = models.CharField(max_length=500,null=True, blank=True)
    Compliance_Training_Status = models.CharField(max_length=500, null=True, blank=True)

    # EnterpriseHireDate=models.CharField(null=True,max_length=500)

    # AssignmentStatusType=models.CharField(max_length=255,null=True)
    # PersonType=models.CharField(max_length=255,null=True)
    # AssignmentType=models.CharField(max_length=255,null=True)
    # EmployeePhoneNumber=models.CharField(max_length=255,null=True)
    # EmailAddress=models.CharField(max_length=255,null=True)
    # GradeName=models.CharField(max_length=255,null=True)
    # BusinessArea=models.CharField(max_length=255,null=True)
    # CostCenter=models.CharField(max_length=255,null=True)
    # CompanyCode=models.CharField(max_length=255,null=True)
    # LineManagerName=models.CharField(max_length=255,null=True)
    # LineManagerPersonNumber=models.CharField(max_length=255,null=True)
    # LineManagerPositionCode=models.CharField(max_length=255,null=True)
    # payroll=models.CharField(max_length=255,null=True)
    # COE=models.CharField(max_length=255,null=True)
    # Role=models.CharField(max_length=255,null=True)
    # Vertical=models.CharField(max_length=255,null=True)
    # dept=models.ForeignKey(DeptMaster,on_delete=models.CASCADE,related_name="dept_employees")

    def __str__(self):
        return self.EmployeeName

    def get_employee_progress(self):
        from review.models import Category
        total_progress = 0.0
        all_category_count = Category.objects.all().count()
        all_category_percent = 100 / all_category_count
        pending_review = self.employee_review.filter(final_status=False)
        if pending_review.exists():
            pending_review_obj = pending_review.last()
            total_progress = all_category_percent * pending_review_obj.employee_root_category_review.all().count()
        return math.ceil(total_progress)
        # return 50

    def check_employee_is_new_joiner(self):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        enter_prise_hire_date = datetime.strptime(self.DateOfJoin, '%d.%m.%Y').date()
        today_date = datetime.today().date()
        three_months_back_date = today_date - relativedelta(months=3)
        if three_months_back_date <= enter_prise_hire_date <= today_date:
            return True
        return False

    def get_employee_review_draft_exists(self):
        # all_category_count = Category.objects.all().count()
        if self.employee_review.filter(final_status=False).exists():
            return True
        return False

    def check_all_category_data_fill_up(self):
        from review.models import Category
        all_category_count = Category.objects.all().count()
        if self.employee_review.filter(final_status=False).exists():
            employee_pending_review_obj = self.employee_review.filter(final_status=False).last()
            employee_submit_review_category_count = employee_pending_review_obj.employee_root_category_review.all().count()
            if all_category_count == employee_submit_review_category_count:
                return True
        return False

    def get_employee_last_review_date(self):
        employee_review = self.employee_review.filter(final_status=True)
        if employee_review.exists():
            return employee_review.last().submitted_date
        return None

    def get_employee_submitted_review(self):
        all_employee_review = self.employee_review.filter(final_status=True).order_by("-id")
        return all_employee_review

    def get_employee_last_review(self):
        all_employee_review = self.employee_review.filter(final_status=True).order_by("-id")
        if all_employee_review:
            return all_employee_review.last().employee_root_category_review.all()
        return None

    def check_employee_last_review_exists(self):
        all_employee_last_review = self.employee_review.filter(final_status=True)
        if all_employee_last_review.exists():
            return True
        return False

    def get_employee_last_root_review(self):
        employee_last_review = self.employee_review.filter(final_status=True).order_by("-id")
        if employee_last_review.exists():
            return employee_last_review.first()
        return None

    def check_employee_final_submit_review_exists(self):
        if self.employee_review.filter(final_status=True).exists():
            return True
        return False


    class meta:
        db_table = "EmployeeMaster"




