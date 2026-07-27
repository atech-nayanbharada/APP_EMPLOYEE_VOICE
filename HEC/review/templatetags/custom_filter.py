from django import template
from review.models import EmpReviewQuesAns
register=template.Library()


@register.filter
def check_question_exists(employee_obj, question_template_obj):
    all_employee_last_draft_review_obj = employee_obj.employee_review.filter(final_status=False)
    if all_employee_last_draft_review_obj.exists():
        employee_last_draft_review_obj = all_employee_last_draft_review_obj.first()
        # print(employee_last_draft_review_obj, "review objj")
        last_review_question = employee_last_draft_review_obj.employee_root_category_review.filter(employee_review_ques_ans__Question=question_template_obj)
        if last_review_question.exists():
            emp_review_que_ans_obj = EmpReviewQuesAns.objects.filter(Review__employee_root__Employee=employee_obj,
                                                                     Question=question_template_obj,
                                                                     Review__employee_root=employee_last_draft_review_obj).first()
            return "question_exists", emp_review_que_ans_obj.Ans, emp_review_que_ans_obj.remark, emp_review_que_ans_obj.data_is_upload_backend
    return "question_not_exists", "not_ans", "no_remark"

    # employee_question_filter_data = employee_obj.employee_review.filter(employee_review_ques_ans__Question=question_template_obj)
    # if employee_question_filter_data.exists():
    #     emp_review_que_ans_obj = EmpReviewQuesAns.objects.filter(Review__Employee=employee_obj,
    #                                                              Question=question_template_obj).first()
    #     return "question_exists", emp_review_que_ans_obj.Ans, emp_review_que_ans_obj.remark
    # return "question_not_exists", "not_ans", "no_remark"


@register.filter
def employee_review_comment(employee_obj, category_name):
    all_employee_last_draft_review_obj = employee_obj.employee_review.filter(final_status=False)
    if all_employee_last_draft_review_obj.exists():
        employee_last_draft_review_obj = all_employee_last_draft_review_obj.first()
        employee_category_review = employee_last_draft_review_obj.employee_root_category_review.filter(
            Category__CategoryName=category_name)
        if employee_category_review.exists():
            return employee_category_review.first().AdditionalComment
    return None
    # employee_category_review = employee_obj.employee_review.filter(Category__CategoryName=category_name)
    # if employee_category_review.exists():
    #     return employee_category_review.first().AdditionalComment
    # return None


@register.filter
def employee_review_last_modified(employee_obj, category_name):
    employee_category_review = employee_obj.employee_review.filter(Category__CategoryName=category_name)
    if employee_category_review.exists():
        return employee_category_review.first().modified
    return None


@register.filter
def employee_last_review_question_ans(employee_obj, question_template_obj):
    all_employee_last_draft_review_obj = employee_obj.employee_review.filter(final_status=True).order_by('-id')
    if all_employee_last_draft_review_obj.exists():
        employee_last_draft_review_obj = all_employee_last_draft_review_obj.first()
        last_review_question = employee_last_draft_review_obj.employee_root_category_review.filter(
            employee_review_ques_ans__Question=question_template_obj)
        if last_review_question.exists():
            emp_review_que_ans_obj = EmpReviewQuesAns.objects.filter(Review__employee_root__Employee=employee_obj,
                                                                     Question=question_template_obj,
                                                                     Review=last_review_question.first()).last()
            return "question_exists", emp_review_que_ans_obj.Ans, emp_review_que_ans_obj.remark
    return "question_not_exists", "not_ans", "no_remark", "no"



@register.filter
def employee_last_review_comment(employee_obj, category_name):
    all_employee_last_draft_review_obj = employee_obj.employee_review.filter(final_status=True)
    if all_employee_last_draft_review_obj.exists():
        employee_last_draft_review_obj = all_employee_last_draft_review_obj.last()
        employee_category_review = employee_last_draft_review_obj.employee_root_category_review.filter(
            Category__CategoryName=category_name)
        if employee_category_review.exists():
            return employee_category_review.first().AdditionalComment
    return ""

@register.filter
def review_ews_status(employee_obj):
    review_ews_status = "Green"
    employee_draft_review = employee_obj.employee_review.filter(final_status=False)
    if employee_draft_review.exists():
        employee_draft_review = employee_draft_review.last()
        review_ews_status = employee_draft_review.get_review_positive_negative_status
    return review_ews_status


@register.filter
def check_category_data_fill(employee_obj, category):
    employee_last_obj = employee_obj.employee_review.filter(final_status=False).first()
    if employee_last_obj:
        if employee_last_obj.employee_root_category_review.filter(Category=category).exists():
            return True
    return False


