import os

from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

static_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "/templates"))

templates = Jinja2Templates(directory="templates")


@router.get('/signin', response_class=HTMLResponse)
async def sing_in_form(request: Request):
    return templates.TemplateResponse(request=request,
                                      name='sign_in.html',
                                      )


user_dict = {
    "yoonjae": "qwer"
}


@router.post('/signin', response_class=HTMLResponse)
async def login_form_post(request: Request,
                          email: str = Form(...),
                          password: str = Form(...)):

    if (email in user_dict) and (password == user_dict[email]):
        return templates.TemplateResponse("success.html",
                                          {"request": request})

    else:
        return templates.TemplateResponse("sign_in.html", {"request": request})

departments = [
    {"value": "hr", "text": "Human Resources"},
    {"value": "it", "text": "Information Technology"},
    {"value": "marketing", "text": "Marketing"},
    {"value": "sales", "text": "Sales"},
    {"value": "ddd", "text": "ddd"}
]


@router.get("/signup")
async def signup_form(request: Request):
    return templates.TemplateResponse('sign_up.html',
                                      context={'request': request, "departments": departments})


@router.post("/signup")
async def signup_form_post(request: Request):
    return templates.TemplateResponse('success.html',
                                      context={'request': request})
