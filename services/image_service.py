import random
import string
from fastapi import UploadFile
from sqlmodel import Session, select
from sqlalchemy.engine import Engine

from database.models import Image

class ImageService:

    def __init__(self,engine: Engine):
        self.engine = engine


    async def save_image(self,file: UploadFile):
        new_name = self.format_name(
            self.convert_type(file.content_type)
        )
        url = f"http://localhost:8000/images/{new_name}"
        real_path = f"./media/{new_name}"

        with open(real_path,'wb') as save_file:
            content = await file.read()

            save_file.write(
                content
            )

        image = Image(
            name=new_name,
            url=url,
            realPath=real_path,
            contentType=file.content_type
        )
        print(image)

        with Session(self.engine) as session:
            session.add(image)
            session.commit()
            session.refresh(image)
            session.close()


        return {
            "data": {
                "url": image.url
            }
        }
    
    def format_name(self, content_type: str):
        characters = string.ascii_lowercase + string.digits
        file_name = ''.join(random.choice(characters) for _ in range(10)) + f".{content_type}"
        return file_name


    def convert_type(self,content_type):
        IMAGE_TYPE = {
            "image/jpeg": 'jpeg'
        }

        return IMAGE_TYPE.get(content_type,None)

    async def get_image(self,file_name: str):
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image = session.exec(stateman).first()
            session.close()
            return image
        
    def get_images(self):
        with Session(self.engine) as session:
            # query is decrapeated
            stateman = select(Image)
            images = session.exec(stateman).all()
            session.close()
            return images

    async def update_image(self,file_name: str,image: Image):
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image = session.exec(stateman).first()

            if not image:
                return None

            image.name = image.name
            image.url = image.url
            image.realPath = image.realPath
            image.contentType = image.contentType

            session.add(image)
            session.commit()
            session.refresh(image)

            session.close()
            return image


    def delete_image(self,file_name: str):
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image = session.exec(stateman).first()

            if not image:
                return None

            session.delete(image)
            session.commit()
            session.close()
            return image