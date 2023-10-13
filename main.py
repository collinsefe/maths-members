import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

from utils.azure_sql_database import *
from utils.jiraAPIWrapper import *

import uvicorn
from pydantic import BaseModel

#from sqlalchemy import *

# from starlette.responses import HTMLResponse



app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/imgs", StaticFiles(directory="imgs"), name='img_avatar2.jpg')


@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_response(request: Request,
                            lastname: str = Form(...),
                            firstname: str = Form(...),
                            email: str = Form(...),
                            username: str = Form(...),
                            dob = Form(...),
                            gender: str = Form(...),
                            psw: str = Form(...), psw_repeat: str = Form(...)
                            ):

    try:
        insert_into_table(lastname, firstname, email, username, dob, gender)

    except:
        return "User Already Exist"

    return


@app.get("/forgot_password", response_class=HTMLResponse)
def forgot_password(request:Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})


@app.post("/forgot_password")
async def password(request: Request, email: str = Form(...),
                   username: str = Form(...)):
    print(username, email)

    return read_from_table(username)
    #return "If your email is registered with us, a reset password email will be sent to you"


@app.get("/contact_us", response_class=HTMLResponse)
async def contact_us(request: Request):

    return templates.TemplateResponse("contact_us.html", {"request": request})


@app.post("/contact_us")
async def contact_us(request: Request, firstname: str = Form(...),
                     lastname: str = Form(...),
                     email: str = Form(...),
                     phone: str = Form(...),
                     summary: str = Form(...),
                     detail: str = Form(...),
                     username: str = Form(...)):
    print(firstname, lastname, detail, phone, email) ### Create JIRA ticket logging
    from utils.jira_info import fields
    fields["project"]["key"] = "MOVIES"
    fields["issuetype"]["name"] = "Task"
    fields["customfield_10043"] = email
    fields["customfield_10040"] = phone
    fields["summary"] = summary
    fields["description"] = detail
    fields["customfield_10034"] = [f"{firstname}-{lastname}"]
    fields["customfield_10041"] = username

    print(fields)
    
    
    moviejira = JiraAPI.create_conn()
    moviejira.create_issue(fields)
    

    return templates.TemplateResponse("thank-you.html", {"request": request})



# # main.py
# import os
# import sqlalchemy

# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy import Column, Integer, String, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from starlette.responses import HTMLResponse

# app = FastAPI()

# DATABASE_URL = os.environ['DATABASE_URL']
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()


# class Message(Base):
#     __tablename__ = "messages"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, index=True)
#     message = Column(String, index=True)


# # Create the table in the database
# Base.metadata.create_all(bind=engine)


# class MessageIn(BaseModel):
#     name: str
#     email: str
#     message: str


# @app.post("/messages/", response_model=MessageIn)
# def create_message(message: MessageIn):
#     db_message = Message(**message.model_dump())
#     db = SessionLocal()
#     db.add(db_message)
#     db.commit()
#     db.refresh(db_message)
#     db.close()
#     return db_message


# @app.get("/healthcheck/", response_model=str)
# def healthcheck():
#     return "OK"


# if __name__ == "__main__":
#     try:
#         port = os.environ.get("PORT", "5000")
#         port = int(port)
#     except ValueError:
#         port = 5000
#     uvicorn.run("main:app", host='0.0.0.0', port=port, log_level="info")

