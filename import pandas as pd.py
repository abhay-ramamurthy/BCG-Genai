import pandas as pd
import re

#
final_report = pd.read_csv('final_report.csv')
summary_report = pd.read_csv('Summary_final_report.csv')

def financial_chatbot(query, company_input, fiscal_year):
    
    query = query.lower()
    patterns = {
        "total revenue": r"total revenue",
        "net income": r"net income",
        "total assets": r"total assets",
        "total liabilities": r"total liabilities",
        "cash flow from operating activities": r"cash flow from operating activities",
        "revenue growth": r"revenue growth",
        "net income growth": r"net income growth",
        "assets growth": r"assets hiigrowth",
        "liabilities growth": r"liabilities growth",
        "cash flow from operations growth": r"cash flow from operations growth",
        "year by year average revenue growth rate": r"average revenue growth",
        "year by year average net income growth rate": r"average net income growth",
        "year by year average assets growth rate": r"average assets growth",
        "year by year average liabilities growth rate": r"average liabilities growth",
        "year by year average cash flow from operations growth rate": r"average cash flow from operations growth"
    }
    
    for metric, pattern in patterns.items():
        if re.search(pattern, query):
            metric_key = metric
            break
    else:
        return "Sorry, I couldn't understand your query. Please try again."

    if 'average' not in metric_key:
        data_value = final_report[(final_report['Year'] == fiscal_year) & (final_report['Company'] == company_input)][metric_key.title()].values[0]
        response = f"The {metric_key.title()} for {company_input} for fiscal year {fiscal_year} is ${data_value}."
    else:
        data_value = summary_report[(summary_report['Company'] == company_input)][metric_key.title().replace("Year By Year ", "")].values[0]
        response = f"The {metric_key.title()} from 2021 to 2023 for {company_input} is {data_value}(%)."

    return response

# Test the chatbot
def start_chatbot_session():
    company_input = None
    fiscal_year = None

    while True:
        print("----------------------------------------------------------------------------")
        user_input = input("\nEnter 'Hi' to start the chatbot session; type 'exit' to quit: ").lower()
        if user_input == "exit":
            print("Goodbye!")
            break
        elif user_input == "hi":
            print("\nHello! Welcome to AI Driven Financial Chatbot!!!")
            print("\nI can help you with your financial queries")
            if not company_input:
                print("Please select the company name from below: -")
                print("\n1. Microsoft \n2. Tesla \n3. Apple")
                company_input = input("Enter company name: ").capitalize()
                if company_input not in ['Apple', 'Microsoft', 'Tesla']:
                    print("Invalid Company Name. Please check and enter correct company name by starting the chatbot session again")
                    continue
            if not fiscal_year:
                print("\nThe data for the fiscal year 2023, 2022, and 2021 is currently available")
                fiscal_year = int(input("Enter the fiscal year for the selected company: "))
                if fiscal_year not in [2023, 2022, 2021]:
                    print("Please enter a valid fiscal year by starting the chatbot session again")
                    continue
        else:
            print("Please enter 'Hi' properly to start the chatbot session.")
            continue
        
        query = input("\nPlease enter your financial query: ")
        response = financial_chatbot(query, company_input, fiscal_year)
        print(response)

start_chatbot_session()
