import secrets
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from weasyprint import HTML
from starlette.middleware.sessions import SessionMiddleware
from typing import List
from optimizer import best_fit

app = FastAPI()

# Set up secret key to allow for user-specific states
secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-form")
async def run_optimizer(
    request: Request,
    depth: float = Form(),
    kerf: float = Form(),
    stocks_lengths: List[float] = Form(...),
    stocks_quantities: List[int] = Form(...),
    cuts_lengths: List[float] = Form(...),
    cuts_quantities: List[int] = Form(...),
    cuts_left_wall_angles: List[float] = Form(...),
    cuts_right_wall_angles: List[float] = Form(...)
):  
    # Replace empty angle values with 180 while keeping valid numbers
    cuts_left_wall_angles = [180 if angle == 0 else angle for angle in cuts_left_wall_angles]
    cuts_right_wall_angles = [180 if angle == 0 else angle for angle in cuts_right_wall_angles]

    # Allow empty stock quantities to represent an essentially infinite quantity (input max is 9999)
    stocks_quantities = [9999 if quantity == 0 else quantity for quantity in stocks_quantities]

    # Sort cuts into stocks leaving as little spare as possible
    result = best_fit(
        depth,
        kerf,
        stocks_lengths, 
        stocks_quantities, 
        cuts_lengths, 
        cuts_quantities, 
        cuts_left_wall_angles, 
        cuts_right_wall_angles
    )

    # Save the result in the session
    request.session["result"] = result

    return templates.TemplateResponse("result.html", {"request": request, "result": result})

@app.get("/download-pdf/")
async def download_pdf(request: Request):
    # Retrieve the result from the session
    result = request.session.get("result")

    # Render HTML Template
    template = templates.get_template("result.html")
    html_content = template.render({"request": request, "result": result})

    # Convert to PDF
    pdf_bytes = HTML(string=html_content).write_pdf()

    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": "attachment; filename=page.pdf"}
    )
