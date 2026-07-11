from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import register_user, get_user_by_email
from models.expense_model import (
    add_expense,
    get_user_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense
)
from models.category_model import get_all_categories
from models.income_model import (
    add_income,
    get_user_income,
    get_income_by_id,
    update_income,
    delete_income
)
from models.budget_model import set_budget
from models.dashboard_model import (
    get_dashboard_data,
    get_category_expense,
    get_monthly_expense,
    get_budget,
    get_budget_details,
    get_recent_transactions,
    get_budget_percentage,
    generate_insight,
    save_insight,
    highest_expense_category,
    predict_next_month_expense,
    save_prediction,
    detect_anomaly
)
from ml.prediction import (
    predict_next_month_expense,
    save_prediction
)
from datetime import datetime
import csv
from flask import Response
from utils.pdf_generator import generate_expense_pdf
from models.expense_model import get_all_expenses
from flask import send_file
import os




app = Flask(__name__)
app.secret_key = "expense_tracker_secret_key"





@app.route("/")
def home():
    return render_template("index.html")






@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        register_user(full_name, email, hashed_password)

        user = get_user_by_email(email)

        session["user_id"] = user[0]
        session["user_name"] = user[1]

        return redirect(url_for("dashboard"))

    return render_template("register.html")






@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user:

            if check_password_hash(user[3], password):

                session["user_id"] = user[0]
                session["user_name"] = user[1]

                return redirect(url_for("dashboard"))

            else:
                return "<h2>Incorrect Password!</h2>"

        else:
            return "<h2>User Not Found!</h2>"

    return render_template("login.html")





@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    total_income, total_expense, balance = get_dashboard_data(
        session["user_id"]
    )
    budget = get_budget(session["user_id"])
    budget_percentage = get_budget_percentage(
       session["user_id"]
    )
    if budget_percentage < 70:
        progress_color = "bg-success"
    elif budget_percentage < 90:
        progress_color = "bg-warning"
    else:
        progress_color = "bg-danger"

    insight = generate_insight(budget_percentage)
    if budget_percentage <= 100:
        budget_status = "✅ You are within your budget."
    else:
        budget_status = "🚨 You have exceeded your budget."
    top_category = highest_expense_category(
    session["user_id"]
    )
    save_insight(
    session["user_id"],
    insight
    )
    
    recent_transactions = get_recent_transactions(session["user_id"])




    # Pie Chart Data
    chart_data = get_category_expense(session["user_id"])

    labels = []
    values = []

    for row in chart_data:
        labels.append(row[0])
        values.append(float(row[1]))

    # Monthly Expense Trend
    monthly_data = get_monthly_expense(session["user_id"])

    month_labels = []
    month_values = []

    for row in monthly_data:
        month_labels.append(row[0])
        month_values.append(float(row[1]))

    predicted_expense = predict_next_month_expense(
    session["user_id"]
    )    
    save_prediction(
    session["user_id"],
    predicted_expense
    )
    anomaly = detect_anomaly(
    session["user_id"]
    )
    today = datetime.now().strftime("%d %B %Y")
    return render_template(
    "dashboard.html",
    total_income=total_income,
    total_expense=total_expense,
    balance=balance,
    today=today,
    budget=budget,
    labels=labels,
    values=values,
    month_labels=month_labels,
    month_values=month_values,
    recent_transactions=recent_transactions,
    predicted_expense=predicted_expense,
    budget_percentage=budget_percentage,
    progress_color=progress_color,
    insight=insight,
    top_category=top_category,
    anomaly=anomaly,
    budget_status=budget_status
)






@app.route("/add-expense", methods=["GET", "POST"])
def add_expense_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        user_id = session["user_id"]

        category_id = request.form["category_id"]
        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        expense_date = request.form["expense_date"]
        description = request.form["description"]

        add_expense(
            user_id,
            category_id,
            amount,
            payment_method,
            expense_date,
            description
        )

        return redirect(url_for("view_expenses"))

    categories = get_all_categories()

    print("Categories:", categories)
    return render_template(
        "expenses/add_expense.html",
        categories=categories
    )





@app.route("/view-expenses")
def view_expenses():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    expenses = get_user_expenses(user_id)

    return render_template(
        "expenses/view_expenses.html",
        expenses=expenses
    )






@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        category_id = request.form["category_id"]
        amount = request.form["amount"]
        payment_method = request.form["payment_method"]
        expense_date = request.form["expense_date"]
        description = request.form["description"]

        update_expense(
            expense_id,
            category_id,
            amount,
            payment_method,
            expense_date,
            description
        )

        return redirect(url_for("view_expenses"))

    expense = get_expense_by_id(expense_id)

    categories = get_all_categories()

    return render_template(
        "expenses/edit_expense.html",
        expense=expense,
        categories=categories
    )






@app.route("/delete-expense/<int:expense_id>")
def delete_expense_route(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_expense(expense_id)

    return redirect(url_for("view_expenses"))






@app.route("/add-income", methods=["GET", "POST"])
def add_income_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        user_id = session["user_id"]
        amount = request.form["amount"]
        source = request.form["source"]
        income_date = request.form["income_date"]
        description = request.form["description"]

        add_income(
            user_id,
            amount,
            source,
            income_date,
            description
        )

        return redirect(url_for("view_income"))

    return render_template("income/add_income.html")






@app.route("/view-income")
def view_income():

    if "user_id" not in session:
        return redirect(url_for("login"))

    income = get_user_income(session["user_id"])

    return render_template(
        "income/view_income.html",
        income=income
    )





@app.route("/edit-income/<int:income_id>", methods=["GET", "POST"])
def edit_income(income_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        update_income(
            income_id,
            request.form["amount"],
            request.form["source"],
            request.form["income_date"],
            request.form["description"]
        )

        return redirect(url_for("view_income"))

    income = get_income_by_id(income_id)

    return render_template(
        "income/edit_income.html",
        income=income
    )



@app.route("/delete-income/<int:income_id>")
def delete_income_route(income_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_income(income_id)

    return redirect(url_for("view_income"))





@app.route("/set-budget", methods=["GET", "POST"])
def set_budget_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        month = request.form["month"]
        year = request.form["year"]
        budget_amount = request.form["budget_amount"]

        print("Budget Entered =", budget_amount)

        set_budget(
            session["user_id"],
            month,
            year,
            budget_amount
            )

       

        return redirect(url_for("view_budget"))

    return render_template("budget/set_budget.html")




@app.route("/view-budget")
def view_budget():

    if "user_id" not in session:
        return redirect(url_for("login"))

    budget = get_budget_details(session["user_id"])

    return render_template(
        "budget/view_budget.html",
        budget=budget
    )


@app.route("/export-expenses")
def export_expenses():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_user_expenses(session["user_id"])

    def generate():
        data = csv.writer(open("temp.csv", "w", newline=""))

    output = []

    output.append("Category,Amount,Payment Method,Date,Description\n")

    for expense in expenses:
        output.append(
            f"{expense[1]},{expense[2]},{expense[3]},{expense[4]},{expense[5]}\n"
        )

    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=expenses.csv"
        }
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))





@app.route("/export-pdf")
def export_pdf():

    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_all_expenses(session["user_id"])

    filename = "expense_report.pdf"

    generate_expense_pdf(expenses, filename)

    return send_file(
        filename,
        as_attachment=True
    )




if __name__ == "__main__":
    app.run(debug=True)




















