
from sqlalchemy.orm import Session
from models.image import Image
class ImageCRUD:
    def __init__(self,db: Session):
        self.db = db
    def create_image(self, name: str, description: str, data: bytes, group: str = "default_group"):
        image = Image(name=name, description=description,data=data,group=group,)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image
    def get_image(self, image_id: int):
        return self.db.query(Image).filter(Image.id == image_id).first()
    def get_all_images(self):
        return self.db.query(Image).all()
