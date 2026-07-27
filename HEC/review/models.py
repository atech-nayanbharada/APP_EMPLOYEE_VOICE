from django.db import models
from django_extensions.db.models import TimeStampedModel,ActivatorModel
from user.models import CustomUser
from common.models import EmployeeMaster
# Create your models here.


class Category(TimeStampedModel,ActivatorModel):
    CategoryName=models.CharField(max_length=500)

    def __str__(self):
        return self.CategoryName


class CategoryQuestion(TimeStampedModel,ActivatorModel):
    TEXT = 'text'
    BOOLEAN = 'boolean'
    POSITIVE = "positive"
    NEGATIVE = 'negative'
    QUESTION_TYPE_LIST = ((POSITIVE, 'Positive'), (NEGATIVE, 'Negative'))
    AnsType = ((TEXT, "Text"), (BOOLEAN, "Boolean"))
    Question = models.CharField(max_length=500)
    QuestionType = models.CharField(max_length=500, choices=AnsType)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_question")
    # QUESTION_TYPE = models.CharField(max_length=10, choices=QUESTION_TYPE_LIST, null=True, blank=True)

    def __str__(self):
        return self.Question


class EmpReviewRoot(TimeStampedModel, ActivatorModel):
    final_status = models.BooleanField(default=False)
    Employee = models.ForeignKey(EmployeeMaster, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="employee_review")
    SubmittedBy = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="user_employee_review")
    submitted_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.Employee.EmployeeName}"

    def get_review_positive_negative_status(self):
        ans_yes_list = []
        ans_no_list = []
        ans_n_a_list = []
        total_percentage_of_yes = 0.0
        all_category = Category.objects.exclude(CategoryName="EWS")
        total_question_count = CategoryQuestion.objects.filter(Category__in=all_category).count()
        all_category_review = self.employee_root_category_review.exclude(Category__CategoryName="EWS")

        for category_review_obj in all_category_review:
            for question_ans_obj in category_review_obj.employee_review_ques_ans.all():
                if question_ans_obj.Ans == "Yes":
                    ans_yes_list.append(question_ans_obj.Question.id)
                elif question_ans_obj.Ans == "No":
                    ans_no_list.append(question_ans_obj.Question.id)
                elif question_ans_obj.Ans == "N/A":
                    ans_n_a_list.append(question_ans_obj.Question.id)
                else:
                    pass

        total_percentage_of_yes = len(ans_yes_list)/total_question_count*100
        print(total_percentage_of_yes, "total percentage of yes")
        if total_percentage_of_yes < 30:
            return "Red"
        elif 30 <= total_percentage_of_yes <= 80:
            return "Amber"
        else:
            return "Green"


class EmployeeReview(TimeStampedModel,ActivatorModel):
    employee_root = models.ForeignKey(EmpReviewRoot, on_delete=models.SET_NULL,null=True,blank=True, related_name="employee_root_category_review")
    Category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="category_employee_review")
    # SubmittedBy=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name="user_employee_review")
    # Employee=models.ForeignKey(EmployeeMaster,on_delete=models.SET_NULL,null=True,blank=True,related_name="employee_review")
    AdditionalComment=models.TextField(null=True)

    # DirectMail=models.BooleanField(default=False)
    # HodMail=models.BooleanField(default=False)
    # CoeMail=models.BooleanField(default=False)
    # GroupHr=models.BooleanField(default=False)
    # DirectMailIds=models.TextField(null=True)
    # CoeMailIds = models.TextField(null=True)
    # HodMailIds = models.TextField(null=True)
    # GroupHrIds = models.TextField(null=True)


class EmpReviewQuesAns(TimeStampedModel,ActivatorModel):
    TEXT = 'text'
    BOOLEAN = 'boolean'
    AnsTypes = ((TEXT, "Text"), (BOOLEAN, "Boolean"))
    Review = models.ForeignKey(EmployeeReview, on_delete=models.SET_NULL,null=True,blank=True, related_name="employee_review_ques_ans")
    Question = models.ForeignKey(CategoryQuestion, on_delete=models.SET_NULL, null=True,blank=True, related_name="cat_question_employee_review")
    Ans=models.CharField(max_length=500)
    AnsType=models.CharField(max_length=500,choices=AnsTypes)
    remark = models.TextField(null=True)
    data_is_upload_backend = models.BooleanField(default=False)


