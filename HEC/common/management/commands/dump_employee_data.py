import os
import pandas
import json
from django.core.management.base import BaseCommand, CommandError
from HEC.settings import BASE_DIR
from common.models import EmployeeMaster


class Command(BaseCommand):
    """ this command is used for employee data dump """

    def handle(self, *args, **options):
        file_name = "HR_sampark_13_03_2024.xlsx"
        master_data_dir = os.path.join(BASE_DIR, "static\MasterData\employee_master")
        excel_data_df = pandas.read_excel(f"{master_data_dir}\{file_name}")
        # print(excel_data_df)
        # print(excel_data_df.columns, "gdjjd")
        # print(excel_data_df.to_dict('records'), "dd")
        all_employee_data = excel_data_df.to_dict('records')
        for employee_data in all_employee_data:

            employee_code = str(employee_data.get('Employee Code')).replace("nan","")
            employee_name = str(employee_data.get('Name of Employee')).replace("nan","")
            position_code = str(employee_data.get('Position Code')).replace("nan","")
            position = str(employee_data.get('Designation (Position Name)')).replace("nan","")
            grade_code = str(employee_data.get('Grade code')).replace("nan","")
            employee_status = str(employee_data.get('Employment Status')).replace("nan","")
            employee_type = str(employee_data.get('Employee Type')).replace("nan","")
            business_unit = str(employee_data.get('Business Unit')).replace("nan","")
            legal_entity = str(employee_data.get('Legal Entity')).replace("nan","")
            dept_as_per_oracle_string = str(employee_data.get('Department as per Oracle string')).replace("nan","")
            dept_reporting_name = str(employee_data.get('Department Reporting Name')).replace("nan","")
            location = str(employee_data.get('Location')).replace("nan","")
            date_of_birth = str(employee_data.get('Date of Birth')).replace("nan","")
            age = str(employee_data.get('Age')).replace("nan","")
            gender = str(employee_data.get('Gender')).replace("nan","")
            marital_status = str(employee_data.get('Marital Status')).replace("nan","")
            date_of_join = str(employee_data.get('Date of Joining')).replace("nan","")
            group_date_of_join = str(employee_data.get('Group Date of Joining')).replace("nan","")
            # date_of_separation = str(employee_data.get('Date of Separation')).replace("nan","")
            date_of_retirement = str(employee_data.get('Date of Retirement')).replace("nan","")
            adani_exp = str(employee_data.get('Adani Experience')).replace("nan","")
            previous_exp = str(employee_data.get('Previous Experience')).replace("nan","")
            total_year_exp = str(employee_data.get('Total Years of Exp')).replace("nan","")
            reporting_manager_emp_id = str(employee_data.get('Reporting Manager (Emp Id)')).replace("nan","")
            reporting_manager_position = str(employee_data.get('Reporting Manager (Position)')).replace("nan","")
            reporting_manager_full_name = str(employee_data.get('Reporting Manager (Full Name)')).replace("nan","")
            hod_emp_id = str(employee_data.get('HOD ( Emp Id)')).replace("nan","").replace(".0","")
            hod_full_name = str(employee_data.get('HOD ( Full Name)')).replace("nan","")
            functional_manager_id = str(employee_data.get('Functional Manager ( Emp ID)')).replace("nan","")
            functional_manager_full_name = str(employee_data.get('Functional Mananger ( Full Name)')).replace("nan","")
            kra_status = str(employee_data.get('KRA Status')).replace("nan","")
            domicile_state = str(employee_data.get('Domicile State')).replace("nan","")

            print(employee_code, "employee code")
            print(employee_name, "employee name")
            # print(position_code, "position Code")
            print(position, "position")
            print(grade_code, "grade code")
            print(employee_status, "employee status")
            print(employee_type, "employee type")
            # print(business_unit, "Bussiness unit")
            print(legal_entity, "legal entity")
            # print(dept_as_per_oracle_string, "dept as per oracle")
            print(dept_reporting_name, "dept reporting name")
            print(location, "location")
            print(date_of_birth, "date of birth")
            # print(age, "age")
            print(gender, "gender")
            # print(marital_status, "marital status")
            print(date_of_join, "date of join")
            print(group_date_of_join, "group date of join")
            # print(date_of_separation, "date of sepration")
            # print(date_of_retirement, "date of retirement")
            print(adani_exp, "adani exp")
            print(previous_exp, "previous exp")
            print(total_year_exp, "total year exp")
            print(reporting_manager_emp_id, "reporting manager emp id")
            print(reporting_manager_position, "reporting manager position")
            print(reporting_manager_full_name, "reporting manager full name")
            print(hod_emp_id, "hod emp id")
            # print(hod_full_name, "hod full name")
            # print(functional_manager_id, "functional manager id")
            # print(functional_manager_full_name, "functional manager full name")
            # print(kra_status, "kra status")
            # print(domicile_state, "domicile state")
            print(" ")


            emp_obj, status = EmployeeMaster.objects.update_or_create(
                EmployeeNumber=employee_code,
                defaults={
                    "EmployeeName": employee_name,
                    # "PositionCode": position_code,
                    "Position": position,
                    "GradeCode": grade_code,
                    "EmployeeStatus": employee_status,
                    "EmployeeType": employee_type,
                    # "BusinessUnit": business_unit,
                    "LegalEntity": legal_entity,
                    # "DepartmentOfOracleString": dept_as_per_oracle_string,
                    "DepartmentReportingName": dept_reporting_name,
                    "Location": location,
                    "DateOfBirth": date_of_birth,
                    # "Age": age,
                    "Gender": gender,
                    # "MaritalStatus": marital_status,
                    "DateOfJoin": date_of_join,
                    "GroupOfDateOfJoin": group_date_of_join,
                    # "DateOfSeparation": date_of_separation,
                    # "DateOfRetirement": date_of_retirement,
                    "AdaniExperience": adani_exp,
                    "PreviousExperience": previous_exp,
                    "TotalYearOfExperience": total_year_exp,
                    "ReportingMangerID": reporting_manager_emp_id,
                    "ReportingMangerPosition": reporting_manager_position,
                    "ReportingMangerFullName": reporting_manager_full_name,
                    "HODEMPID": hod_emp_id,
                    # "HODFullName": hod_full_name,
                    # "FunctionalManagerID": functional_manager_id,
                    # "FunctionalManagerFullName": functional_manager_full_name,
                    # "KRAStatus": kra_status,
                    # "DomicileState": domicile_state
                }

            )
            if emp_obj:
                self.stdout.write(self.style.SUCCESS(f"Employee add successfully. employee code : {emp_obj.EmployeeNumber}- status: {status}"))





