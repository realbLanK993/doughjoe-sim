from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .router import router
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )



@app.get("/test", response_class=HTMLResponse)
async def test_index(request:Request):
    return templates.TemplateResponse(
        request=request,
        name='game/index.html'
    )
