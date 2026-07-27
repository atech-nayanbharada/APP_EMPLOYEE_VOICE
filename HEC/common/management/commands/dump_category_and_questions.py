from django.core.management.base import BaseCommand, CommandError
from review.models import Category, CategoryQuestion


class Command(BaseCommand):
    """ this command is used for category and category question store """
    all_category_question_data = {
        "New Joinee": ["New Joinee?",
                       "Laptop / Desktop/Email id within 2 days of joining?",
                       "Stationery kit/Landline/SIM/Work Station wihtin 2 days joining?",
                       "Probation Confirmation days Overdue?"],
        "PMS": ["KRA input in Oracle PMS",
                "Last year rating communicated",
                "PMS discussion done by manager or not",
                "Mid year Completion Status",
                "Final Year compltetion status"],
        "Policies": ["Confirmation Letter Status",
                     "Handset Policy",
                     "Car policy Query",
                     "Home loan interest subsidy query",
                     "Personal loan policy query",
                     "Leaves Coverage",
                     "Transfer policy query",
                     "Mediclaim policy"],
        "Talent Management": ["Completed 2 years in current job /location",
                              "Are you posted in home town or not?",
                              "Next function aspiration",
                              "Next role aspiration"],
        "L&D": ["No. of training Mandays attended",
                "ABCF Awareness score",
                "Percipio Completion score",
                "Mandatory Trainings status",
                "Trainings / Certification interested"],
        "Others": ["Late sitting report",
                   "Rude behaviour from supervisor",
                   "Help & support from supervisor",
                   "Resolution of the Query done/pending in HR",
                   "Suggestions/improvments/Remarks",
                   "Sufficient interaction with Manager/Function Head",
                   "Sufficient opportunities in interacting with my fellow colleagues",
                   "Is employee expecting promotion?"],
        "EWS": ["Overall EWS Remarks",
                "EWS Status (To be filled by HR – Red/ Amber/ Green)",
                "EWS Major Reason"]
    }

    def handle(self, *args, **options):
        for category in self.all_category_question_data:
            category_object, status = Category.objects.update_or_create(
                CategoryName=category
            )
            self.stdout.write(self.style.SUCCESS(
                f"Category object create successfully. category: -- {category_object} - status: {status}"))
            for cat_question in self.all_category_question_data.get(category):
                category_question_object, que_status = CategoryQuestion.objects.update_or_create(
                    Category=category_object,
                    Question=cat_question,
                    QuestionType=CategoryQuestion.BOOLEAN,

                )
                self.stdout.write(self.style.SUCCESS(
                    f"Category question create successfully. category: -- {category_question_object} - status: {que_status}"))
