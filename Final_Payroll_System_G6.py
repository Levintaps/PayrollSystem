import re
from calendar import monthrange  # Add this line

# Group: 6
# Group Leader:
# Members:

employee_db = {}

def main_menu():
    print("Welcome to the Simple Payroll System")
    print("1) Payroll")
    print("2) Register Employee")
    print("3) View Employee")
    print("4) Exit")

def is_valid_employee_id(employee_id):
    return employee_id in employee_db

def is_valid_pay_period_date(date):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.match(date):
        return False

    year, month, day = map(int, date.split('-'))

    if day != 15 and day != 31:
        return False

    if month < 1 or month > 12:
        return False

    return True

def calculate_payroll(employee_id, pay_period_date, regular_hours, overtime_hours):
    employee = employee_db[employee_id]
    base_rate = employee['salary_rate']

    regular_pay = regular_hours * base_rate
    overtime_pay = overtime_hours * 1.5 * base_rate

    total_gross_pay = regular_pay + overtime_pay

    withholding_tax = 0.15 * total_gross_pay
    sss_contribution = 0.02 * total_gross_pay
    philhealth_contribution = 0.05 * total_gross_pay

    total_net_pay = total_gross_pay - (withholding_tax + sss_contribution + philhealth_contribution)

    print("Payroll Details:")
    print("Employee ID:", employee_id)
    print("Employee Name:", employee['first_name'], employee['last_name'])
    print("Pay Period Date:", pay_period_date)
    print("Regular Hours Worked:", regular_hours)
    print("Overtime Hours Worked:", overtime_hours)
    print("Total Regular Pay:", regular_pay)
    print("Total Overtime Pay:", overtime_pay)
    print("Total Gross Pay:", total_gross_pay)
    print("Deductions:")
    print("Withholding Tax:", withholding_tax)
    print("SSS Contribution:", sss_contribution)
    print("PhilHealth Contribution:", philhealth_contribution)
    print("Total Net Pay:", total_net_pay)

def register_employee(employee_id):
    if is_valid_employee_id(employee_id):
        print("Employee with ID", employee_id, "is already registered.")
        return

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    tin_id = input("Enter 12-Digit TIN ID: ")
    while not re.match(r'^\d{12}$', tin_id):
        print("Invalid TIN ID. It must be a 12-digit number.")
        tin_id = input("Enter 12-Digit TIN ID: ")

    sss_id = input("Enter 10-Digit SSS ID: ")
    while not re.match(r'^\d{10}$', sss_id):
        print("Invalid SSS ID. It must be a 10-digit number.")
        sss_id = input("Enter 10-Digit SSS ID: ")

    philhealth_id = input("Enter 12-Digit PhilHealth ID: ")
    while not re.match(r'^\d{12}$', philhealth_id):
        print("Invalid PhilHealth ID. It must be a 12-digit number.")
        philhealth_id = input("Enter 12-Digit PhilHealth ID: ")

    department_choices = {'1': 'Faculty', '2': 'Non-Faculty'}
    while True:
        print("Choose Department:")
        print("1) Faculty")
        print("2) Non-Faculty")
        department_choice = input("Enter Department Choice (1/2): ")
        if department_choice in department_choices:
            department = department_choices[department_choice]
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2).")

    position_choices = {'1': 'Full-Time', '2': 'Part-Time'}
    while True:
        print("Choose Position:")
        print("1) Full-Time")
        print("2) Part-Time")
        position_choice = input("Enter Position Choice (1/2): ")
        if position_choice in position_choices:
            position = position_choices[position_choice]
            break
        else:
            print("Invalid choice. Please enter a valid option (1/2).")

    salary_rate = float(input("Enter Salary Rate per Hour: "))
    while salary_rate <= 0:
        print("Invalid salary rate. Salary rate must be greater than 0.")
        salary_rate = float(input("Enter Salary Rate per Hour: "))

    employee = {
        'first_name': first_name,
        'last_name': last_name,
        'tin_id': tin_id,
        'sss_id': sss_id,
        'philhealth_id': philhealth_id,
        'department': department,
        'position': position,
        'salary_rate': salary_rate
    }
    employee_db[employee_id] = employee
    print("Employee with ID", employee_id, "has been registered successfully.")

def view_employee(employee_id):
    if not is_valid_employee_id(employee_id):
        print("Employee with ID", employee_id, "is not registered.")
        return

    employee = employee_db[employee_id]
    print("Employee Details:")
    print("Employee ID:", employee_id)
    print("First Name:", employee['first_name'])
    print("Last Name:", employee['last_name'])
    print("TIN ID:", employee['tin_id'])
    print("SSS ID:", employee['sss_id'])
    print("PhilHealth ID:", employee['philhealth_id'])
    print("Assigned Department:", employee['department'])
    print("Job Position:", employee['position'])

    # Check if payroll entries exist for the employee
    if 'payroll_entries' in employee and employee['payroll_entries']:
        print("\nPayroll Entries:")
        for entry in employee['payroll_entries']:
            print("\nPay Period Date:", entry['pay_period_date'])

            # Calculate coverage dates
            start_date = entry['pay_period_date'][:-2] + '01'
            end_date = entry['pay_period_date'][:-2] + str(monthrange(int(entry['pay_period_date'][:4]), int(entry['pay_period_date'][5:7]))[1])
            print("Pay Period Coverage Dates:", start_date, "to", end_date)

            print("Total Regular Hours Worked:", entry['regular_hours'])
            print("Total Overtime Hours Worked:", entry['overtime_hours'])

            base_rate = employee['salary_rate']
            regular_pay = entry['regular_hours'] * base_rate
            overtime_pay = entry['overtime_hours'] * 1.5 * base_rate

            print("\nPayroll Details:")
            print("Total Regular Pay:", regular_pay)
            print("Total Overtime Pay:", overtime_pay)

            total_gross_pay = regular_pay + overtime_pay
            print("Total Gross Pay:", total_gross_pay)

            withholding_tax = 0.15 * total_gross_pay
            sss_contribution = 0.02 * total_gross_pay
            philhealth_contribution = 0.05 * total_gross_pay

            print("\nDeductions:")
            print("Withholding Tax:", withholding_tax)
            print("SSS Contribution:", sss_contribution)
            print("PhilHealth Contribution:", philhealth_contribution)

            total_net_pay = total_gross_pay - (withholding_tax + sss_contribution + philhealth_contribution)
            print("\nTotal Net Pay:", total_net_pay)
    else:
        print("\nNo payroll entries found for this employee.")

    while True:
        another_transaction = input("\nDo another transaction? (yes/no): ")
        if another_transaction.lower() == "yes":
            break
        elif another_transaction.lower() == "no":
            break
        else:
            print("Invalid Input. Please Enter (yes/no)")

    if another_transaction.lower() == "no":
        return
def calculate_payroll(employee_id, pay_period_date, regular_hours, overtime_hours):
    employee = employee_db[employee_id]
    base_rate = employee['salary_rate']

    regular_pay = regular_hours * base_rate
    overtime_pay = overtime_hours * 1.5 * base_rate

    total_gross_pay = regular_pay + overtime_pay

    withholding_tax = 0.15 * total_gross_pay
    sss_contribution = 0.02 * total_gross_pay
    philhealth_contribution = 0.05 * total_gross_pay

    total_net_pay = total_gross_pay - (withholding_tax + sss_contribution + philhealth_contribution)

    # Add the payroll entry to the employee's record
    payroll_entry = {
        'pay_period_date': pay_period_date,
        'regular_hours': regular_hours,
        'overtime_hours': overtime_hours,
        'total_gross_pay': total_gross_pay,
        'withholding_tax': withholding_tax,
        'sss_contribution': sss_contribution,
        'philhealth_contribution': philhealth_contribution,
        'total_net_pay': total_net_pay
    }

    if 'payroll_entries' in employee:
        employee['payroll_entries'].append(payroll_entry)
    else:
        employee['payroll_entries'] = [payroll_entry]

    print("Payroll Details:")
    print("Employee ID:", employee_id)
    print("Employee Name:", employee['first_name'], employee['last_name'])
    print("Pay Period Date:", pay_period_date)
    print("Regular Hours Worked:", regular_hours)
    print("Overtime Hours Worked:", overtime_hours)
    print("Total Regular Pay:", regular_pay)
    print("Total Overtime Pay:", overtime_pay)
    print("Total Gross Pay:", total_gross_pay)
    print("Deductions:")
    print("Withholding Tax:", withholding_tax)
    print("SSS Contribution:", sss_contribution)
    print("PhilHealth Contribution:", philhealth_contribution)
    print("Total Net Pay:", total_net_pay)

while True:
    main_menu()
    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        employee_id = input("Enter Employee ID: ")
        if not is_valid_employee_id(employee_id):
            print("Employee with ID", employee_id, "is not registered. Please Register First.")
            continue
        while True:
            try:
                pay_period_date = input("Enter Pay Period Date (YYYY-MM-DD): ")

                if not re.match(r'\d{4}-\d{2}-\d{2}', pay_period_date):
                    raise ValueError("Invalid input format. Please follow the example (YYYY-MM-DD). Please try again.")

                if not is_valid_pay_period_date(pay_period_date):
                    print("Invalid Pay Period Date. It must be the 15th or the last day of the month.")
                else:
                    break

            except ValueError:
                print("Invalid input format. Please follow the example (YYYY-MM-DD). Please try again.")
                # removed continue

        print("Pay Period Coverage Dates:", "TODO: Calculate coverage dates")

        regular_hours = float(input("Enter Total Regular Hours Worked: "))
        if regular_hours <= 0:
            print("Invalid input. Regular hours must be greater than 0.")
            continue

        overtime_hours = float(input("Enter Total Overtime Hours Worked: "))
        if overtime_hours < 0:
            print("Invalid input. Overtime hours must be non-negative.")
            continue

        calculate_payroll(employee_id, pay_period_date, regular_hours, overtime_hours)

        while True:
            another_transaction = input("Do another transaction? (yes/no): ")
            if another_transaction.lower() == "yes":
                break
            elif another_transaction.lower() == "no":
                break
            else:
                print("Invalid Input. Please Enter (yes/no)")

        if another_transaction.lower() == "no":
            continue

    elif choice == "2":
        while True:
            employee_id = input("Enter Employee ID: ")
            register_employee(employee_id)
            while True:
                another_transaction = input("Do another transaction? (yes/no): ")
                if another_transaction.lower() == "yes":
                    break
                elif another_transaction.lower() == "no":
                    break
                else:
                    print("Invalid Input. Please Enter (yes/no)")

            if another_transaction.lower() == "no":
                break

    elif choice == "3":
        while True:
            employee_id = input("Enter Employee ID: ")
            view_employee(employee_id)
            while True:
                another_transaction = input("Do another transaction? (yes/no): ")
                if another_transaction.lower() == "yes":
                    break
                elif another_transaction.lower() == "no":
                    break
                else:
                    print("Invalid Input. Please Enter (yes/no)")

            if another_transaction.lower() == "no":
                break

    elif choice == "4":
        print("Goodbye")
        break

    else:
        print("Invalid choice. Please enter a valid option (1/2/3/4).")
