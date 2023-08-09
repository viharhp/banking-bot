from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.pdfgen import canvas
from .models import Customer, Account, Transaction, Statement, TransactionEntry, Report, Branch, Loan, CreditCard, BillPayment, Beneficiary, InterestRate, SecurityQuestion, Feedback
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import pickle
import operator

# Sklearn Libraries
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

import random
import nltk
from nltk.stem.lancaster import LancasterStemmer


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if request.POST['password'] == request.POST['confirmPassword']:
                form.save()
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match.")
                return render(request, 'register.html')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user_details = Customer.objects.get(email=email,password=password)
            if user_details:
                request.session['user'] = email
                return redirect('home')
        except:
            return render(request,'404.html')
    return render(request, 'login.html')

def logout_view(request):
    del request.session['User']
    return redirect('login')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required
def customer_detail(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, 'customer_detail.html', {'customer': customer})

@login_required
def account_detail(request, account_number):
    #account = Account.objects.get(account_number=account_number)
    #return render(request, 'account_detail.html', {'account': account})
    return HttpResponse("hello world")

@login_required
def transaction_list(request):
    # account = Account.objects.get(account_number=account_number) <str:account_number>/
    # transactions = Transaction.objects. filter(account=account)
    return render(request, 'transaction_list.html')


@login_required
def deposit_money(request):
    # account = get_object_or_404(Account, account_number=account_number)

    # if request.method == 'POST':
    #     amount = float(request.POST.get('amount'))
    #     if amount > 0:
    #         account.balance += amount
    #         account.save()

    #         # Create a transaction record
    #         transaction = Transaction.objects.create(account=account, transaction_type='D', amount=amount)
    #         transaction.save()

    #         return redirect('transaction_list', account_number=account_number)
    form = DepositMoney()

    if request.method == 'POST':
        form = DepositMoney(request.POST)
        if form.is_valid():
            balance = request.POST.get('amount')
            pass

            return render(request, 'deposit_money.html',{'balance':balance})

    return render(request, 'deposit_money.html')

@login_required
def interac_eTransfer(request):
    # account = get_object_or_404(Account, account_number=account_number)
    # form = WithdrawalForm()

    # if request.method == 'POST':
    #     form = WithdrawalForm(request.POST)
    #     if form.is_valid():
    #         amount = form.cleaned_data['amount']
    #         if amount <= account.balance:
    #             account.balance -= amount
    #             account.save()

    #             # Create a transaction record
    #             transaction = Transaction.objects.create(account=account, transaction_type='W', amount=amount)
    #             transaction.save()

    #             return redirect('transaction_list', account_number=account_number)  {'account': account, 'form': form}


    return render(request, 'interac_e-transfer.html')

@login_required
def transfer_money(request):
    # account = get_object_or_404(Account, account_number=account_number)
    # form = TransferForm()

    # if request.method == 'POST':
    #     form = TransferForm(request.POST)
    #     if form.is_valid():
    #         amount = form.cleaned_data['amount']
    #         recipient_account_number = form.cleaned_data['recipient_account_number']

    #         # Check if the recipient account exists
    #         recipient_account = get_object_or_404(Account, account_number=recipient_account_number)

    #         if amount <= account.balance:
    #             account.balance -= amount
    #             account.save()

    #             recipient_account.balance += amount
    #             recipient_account.save()

    #             # Create a transaction record for sender
    #             transaction_sender = Transaction.objects.create(account=account, transaction_type='T', amount=amount)
    #             transaction_sender.save()

    #             # Create a transaction record for recipient
    #             transaction_recipient = Transaction.objects.create(account=recipient_account, transaction_type='T', amount=amount)
    #             transaction_recipient.save()

                # return redirect('transaction_list', account_number=account_number)  , {'account': account, 'form': form}

    return render(request, 'transfer_money.html')

@login_required
def statement_detail(request, statement_id):
    statement = Statement.objects.get(pk=statement_id)
    entries = TransactionEntry.objects.filter(statement=statement)
    return render(request, 'statement_detail.html', {'statement': statement, 'entries': entries})

@login_required
def report_list(request):
    reports = Report.objects.all()
    return render(request, 'report_list.html', {'reports': reports})

@login_required
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

@login_required
def loan_list(request):
    loans = Loan.objects.filter(account__customer=request.user)
    return render(request, 'loan_list.html', {'loans': loans})

@login_required
def credit_card_detail(request, account_number):
    credit_card = CreditCard.objects.get(account__account_number=account_number)
    return render(request, 'credit_card_detail.html', {'credit_card': credit_card})

@login_required
def bill_payment_list(request):
    bill_payments = BillPayment.objects.filter(customer=request.user)
    return render(request, 'bill_payment_list.html', {'bill_payments': bill_payments})

@login_required
def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.filter(customer=request.user)
    return render(request, 'beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required
def interest_rate_list(request):
    interest_rates = InterestRate.objects.all()
    return render(request, 'interest_rate_list.html', {'interest_rates': interest_rates})

@login_required
def security_question_list(request):
    security_questions = SecurityQuestion.objects.all()
    return render(request, 'security_question_list.html', {'security_questions': security_questions})

@login_required
def feedback_create(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        feedback = Feedback.objects.create(customer=request.user, subject=subject, message=message)
        feedback.save()
        return redirect('feedback_list')
    return render(request, 'feedback_create.html')

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.filter(customer=request.user)
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})


def generate_statement_pdf(request, statement_id):
    statement = get_object_or_404(Statement, id=statement_id)
    entries = TransactionEntry.objects.filter(statement=statement)

    # Create a response object with PDF mime type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="statement.pdf"'

    # Create the PDF object, using the response object as its file
    p = canvas.Canvas(response)

    # Add content to the PDF
    p.setFont('Helvetica', 12)
    p.drawString(30, 750, f"Statement for Account: {statement.account.account_number}")
    p.drawString(30, 720, f"Period: {statement.start_date} - {statement.end_date}")
    p.drawString(30, 690, "Transaction Entries:")

    # Iterate through the transaction entries and add them to the PDF
    y = 660
    for entry in entries:
        p.drawString(30, y, f"Transaction: {entry.transaction}")
        y -= 30

    # Close the PDF object
    p.showPage()
    p.save()

    return response



#Bot


# stemmer = LancasterStemmer()
# le = LabelEncoder()
# tfv = TfidfVectorizer(min_df=1, stop_words='english')
# data = pd.read_csv('BankFAQs.csv')

# with open('trained_model.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# def chatbot(request):
#     stemmer = LancasterStemmer()
#     le = LabelEncoder()
#     tfv = TfidfVectorizer(min_df=1, stop_words='english')
#     data = pd.read_csv('BankFAQs.csv')

#     # with open('trained_model.pkl', 'rb') as model_file:
#     #     model = pickle.load(model_file)

#     # X = data.drop('Answer',axis=1)
#     # y = data['Answer']

#     # X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, random_state=42)
#     # print("X_train shape:",X_train.shape)
#     # print("X_test shape:",X_test.shape)
#     # print("y_train shape:",y_train.shape)
#     # print("y_test shape:",y_test.shape)

#     # tfv.fit(X_train,y_train)
#     if request.method == "POST":
#         user_input = str(request.POST.get("user_input"))
#         transaction = "Transaction"
#         if user_input == transaction:
#             return redirect('transaction_list')
        
#         # Process user input (clean up and tokenization)
#         # def cleanup(sentence):
#         #     word_tok = nltk.word_tokenize(sentence)
#         #     stemmed_words = [stemmer.stem(w) for w in word_tok]
#         #     return ' '.join(stemmed_words)
        
#         # t_usr = tfv.transform([cleanup(user_input.strip().lower())])
#         # class_ = model.predict(t_usr)[0]
#         # class_ = np.atleast_1d(class_)  # Ensure class_ is at least 1D
#         # class_label = le.inverse_transform(class_)[0]
#         # question_set = data[data['Class'] == class_label]



#         # Get the most relevant response from the dataset
#         # cos_sims = []
#         # for question in question_set['Question']:
#         #     sims = cosine_similarity(tfv.transform([question]), t_usr)
#         #     cos_sims.append(sims)

#         # ind = cos_sims.index(max(cos_sims))
#         # response = data['Answer'][question_set.index[ind]]

#         # tfv.fit()
#         print("ifand if c")
#         return render(request,"bot.html")
#     else:
#         print("else ")
#         return render(request, "bot.html")

def chatbot(request):
    response = ''

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        if user_input.lower() == 'hello':
            response = 'Hello! How can I help you?'
        elif user_input.lower() == 'time':
            current_time = datetime.now().strftime('%H:%M:%S')
            response = 'The current time is ' + current_time
        elif user_input.lower() == 'exit':
            response = 'Thank you for using the Bank Chatbot. Goodbye!'
        elif 'deposit' in user_input.lower():
            return redirect("deposit_money")
        elif 'interac' in user_input.lower():
            return redirect("interac_eTransfer")
        elif 'transaction' in user_input.lower():
            return redirect("transaction_list")
        else:

            response = "I'm sorry, I didn't understand. Could you please rephrase?"
    return render(request, 'bot.html', {'response': response})