
from fastapi import  APIRouter, Request, Depends, HTTPException,File, UploadFile
from fastapi.responses import StreamingResponse
from  io import BytesIO
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from CRUD.image_crud import ImageCRUD
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi import Form
from models.image import imageSchema
import base64
router = APIRouter()
# Configure Jinja2Templates
templates = Jinja2Templates(directory="templates")
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None
@router.get("/")
async def read_root():
    return {"Hello": "World"}
@router.get("/newHTML")
async def read_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...),group:str = Form(...),description:str = Form(...), db: Session = Depends(get_db)):
    image_crud = ImageCRUD(db)
    image_data = await file.read()

    image = image_crud.create_image(
        name=file.filename,
        description= description,  # Using content type as description
        group=group,  # Group is now manually entered via request body
        data=image_data
    )
    return {"filename": file.filename, "image_id": image.id}
@router.get("/images/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    image_crud = ImageCRUD(db)
    image = image_crud.get_image(image_id=image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")


    return StreamingResponse(
        BytesIO(image.data),
        headers={"Content-Disposition": f"inline; filename={image.name}"}
    )
@router.get("/get-all-images", response_model=list[imageSchema])
async def get_all_images(db: Session = Depends(get_db)):
    image_crud = ImageCRUD(db)
    images = image_crud.get_all_images()
    response = []
    for img in images:
        encoded_data = base64.b64encode(img.data).decode('utf-8')
        response.append({
            "id": img.id,
            "name": img.name,
            "description": img.description,
            "group": img.group,
            "data": encoded_data
        })
    return response
@router.get("/view-image", response_class=HTMLResponse)
async def view_image_page():
    with open("templates/imageViewer.html") as f:
        return HTMLResponse(content=f.read())
@router.get("/view-all-images", response_class=HTMLResponse)
async def view_all_images_page():
    with open("templates/viewAllImages.html") as f:
        return HTMLResponse(content=f.read())
