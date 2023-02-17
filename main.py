import pickle
from typing import Union

from fastapi import FastAPI

app = FastAPI()
model_pickle = open("./classifier.pkl","rb")
clf=pickle.load(model_pickle)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/predict")
def prediction(loan_req:dict):
    

    if loan_req['Gender']=="Male":
        gender=0
    else:
        gender=1
    if loan_req['Married']=="Unmarried":
        marital_status=0
    else:
        marital_status=1    
    if loan_req['Credit_History']=="Uncleared Debts":
        credit_history=0
    else:
        credit_history=1
    
    applicant_income=loan_req["ApplicantIncome"]
    loan_amt=loan_req['LoanAmount']/1000

    input_data=[[gender,marital_status,applicant_income,loan_amt,credit_history]]
    
    #compute inference

    prediction=clf.predict(input_data)

    if prediction==0:
        pred="Rejected"
    else:
        pred="Approved"

    return {"loan_approval_status":pred}

@app.route("/get_params",methods={"GET"})
def get_application_params():
    parameters={
    "Gender":"<Male/Female>",
    "Married":"<Married/Unmarried>",
    "ApplicantIncome":"Income of applicant",
    "LoanAmount":"Loan amount needed",
    "Credit_History":"<Cleared Debts/Uncleared Debts>"
    }
    return parameters