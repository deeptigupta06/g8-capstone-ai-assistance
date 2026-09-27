import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

applications = {
    "HR Leave Application": [
        "Leave request cannot be submitted",
        "Leave balance is incorrect",
        "Leave approval is pending",
        "Leave calendar is not loading",
        "Leave cancellation is not available",
        "Manager cannot approve leave",
        "Leave request shows validation error",
        "User cannot view previous leave requests",
        "Public holiday is not reflected",
        "Leave application login fails"
    ],
    "Payroll Application": [
        "Payslip is unavailable",
        "Payroll login fails",
        "Salary information is incorrect",
        "Bank details cannot be updated",
        "Payroll submission shows an error",
        "Tax document is unavailable",
        "Employee cannot view payroll history",
        "Payroll page is not loading",
        "Payment status is not displayed",
        "Payroll access is denied"
    ],
    "CRM": [
        "CRM login fails",
        "Customer record cannot be opened",
        "CRM page is not loading",
        "User cannot create a customer record",
        "CRM search returns no results",
        "Customer update cannot be saved",
        "CRM permission error appears",
        "Duplicate customer record is displayed",
        "CRM report cannot be generated",
        "CRM session expires unexpectedly"
    ],
    "CMS": [
        "CMS login fails",
        "Web page cannot be published",
        "CMS editor is not loading",
        "Image cannot be uploaded",
        "User cannot edit content",
        "CMS preview is blank",
        "Publishing workflow is stuck",
        "Content approval is unavailable",
        "CMS page displays an error",
        "User cannot access media library"
    ],
    "Enterprise Applications": [
        "Enterprise application login fails",
        "Application page is not loading",
        "User receives an access denied message",
        "Application session expires",
        "User cannot open a transaction",
        "Application search is not working",
        "User cannot save changes",
        "Application displays a configuration error",
        "Application response is slow",
        "User cannot access application reports"
    ],
    "Oracle": [
        "Oracle login fails",
        "Oracle role is missing",
        "Oracle form does not open",
        "Oracle responsibility is unavailable",
        "Oracle transaction cannot be submitted",
        "Oracle report cannot be generated",
        "Oracle page displays an error",
        "Oracle session expires",
        "Oracle access is denied",
        "Oracle configuration appears incorrect"
    ],
    "PeopleSoft": [
        "PeopleSoft login fails",
        "PeopleSoft page does not load",
        "User cannot submit a transaction",
        "PeopleSoft role is missing",
        "PeopleSoft search returns no result",
        "PeopleSoft form displays an error",
        "User cannot view employee information",
        "PeopleSoft approval is pending",
        "PeopleSoft session expires",
        "PeopleSoft report is unavailable"
    ],
    "Authentication": [
        "User cannot log in",
        "Password reset does not work",
        "User receives repeated login prompts",
        "Multi-factor authentication fails",
        "Single sign-on is unavailable",
        "Account is locked",
        "Authentication error appears",
        "User cannot change password",
        "Login session expires",
        "User receives an invalid credentials message"
    ],
    "Microsoft 365": [
        "Microsoft 365 login fails",
        "Outlook is not synchronising",
        "Teams meeting cannot be created",
        "SharePoint page cannot be opened",
        "OneDrive file cannot be accessed",
        "Microsoft 365 access is denied",
        "User cannot send email",
        "Teams application is not loading",
        "SharePoint upload fails",
        "OneDrive synchronisation is delayed"
    ],
    "VPN and Remote Access": [
        "VPN login fails",
        "VPN connection drops",
        "Remote access is unavailable",
        "VPN profile is missing",
        "Multi-factor authentication fails for VPN",
        "User cannot access internal applications remotely",
        "VPN displays an invalid certificate",
        "VPN connection is very slow",
        "Remote desktop cannot be opened",
        "VPN access is denied"
    ]
}

category_instruction = {
    "HR Leave Application": "Confirm the employee ID, leave dates, leave type, and exact error message.",
    "Payroll Application": "Confirm the employee ID, pay period, payroll screen, and whether the issue affects one or multiple users.",
    "CRM": "Confirm the user ID, CRM module, affected customer record, and exact error message.",
    "CMS": "Confirm the user ID, CMS page, publishing stage, and whether the issue affects one page or multiple pages.",
    "Enterprise Applications": "Confirm the application name, user ID, affected function, and exact error message.",
    "Oracle": "Confirm the Oracle responsibility, form or transaction name, user ID, and error code.",
    "PeopleSoft": "Confirm the PeopleSoft module, user ID, transaction name, and error message.",
    "Authentication": "Confirm the user ID, application, authentication method, and exact error message.",
    "Microsoft 365": (
        "Confirm the user account, affected Microsoft 365 service, "
        "device, browser or application, and exact error message."
    ),
    "VPN and Remote Access": (
        "Confirm the user account, connection method, device, "
        "VPN profile, and exact connection error."
    ),
}

def create_article(kb_number, application, problem):
    category = application

    return {
        "id": f"KB-{kb_number:04d}",
        "title": f"{application} - {problem}",
        "application": application,
        "category": category,
        "problem": problem,
        "symptoms": (
            f"The user reports that {problem.lower()}. "
            "The issue may appear as an error, missing access, or an incomplete transaction."
        ),
        "resolution_steps": [
            "Confirm the user identity and affected application.",
            "Capture the exact error message and time of occurrence.",
            "Ask the user to retry after signing out and signing in again.",
            "Check whether the issue affects other users.",
            "Verify that the user has the required role or access.",
            "Retry the operation using the approved process."
        ],
        "agent_instruction": category_instruction.get(
            category,
            "Confirm the user ID, affected application, exact error message, "
            "time of occurrence, and steps already attempted."
        ),
        "escalation_instruction": (
            f"Escalate to the {application} support team if the issue remains "
            "after the diagnostic checks or if a system-side error is confirmed."
        ),
        "last_updated": "2025-08-01",
        "validity_period_days": 730,
        "url": (
            "https://servicenow.example.com/kb_view.do?"
            f"sysparm_article=KB{kb_number:04d}"
        )
    }

records = []
kb_number = 1

for application, problems in applications.items():
    for problem in problems:
        records.append(
            create_article(kb_number, application, problem)
        )
        kb_number += 1

output_path = DATA_DIR / "knowledge_base.jsonl"

with open(output_path, "w", encoding="utf-8") as file:
    for record in records:
        file.write(json.dumps(record) + "\n")

print(f"Created {len(records)} knowledge-base articles.")
print(f"File: {output_path}")