"""Image service"""
import random
import string
from fastapi import UploadFile
from exceptions.image_exceptions import ImageTypeNotSupportedError
from sqlmodel import Session, select
from sqlalchemy.engine import Engine
from database.models import Image

class ImageService:
    """Image service"""
    engine: Engine | None

    def __init__(self):
        self.engine = None

    def set_engine(self,engine: Engine):
        """Set engine"""
        self.engine = engine


    async def save_image(self,file: UploadFile):
        """Save image"""
        content_type = self.convert_type(file.content_type)

        if not content_type:
            raise ImageTypeNotSupportedError(
                "Image type not supported"
            )

        new_name = self.format_name(
            content_type
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
                "name": image.name,
                "path": "/images/" + image.name
            }
        }

    def format_name(self, content_type: str):
        """Format image name"""
        characters = string.ascii_lowercase + string.digits
        file_name = ''.join(random.choice(characters) for _ in range(10)) + f".{content_type}"
        return file_name


    def convert_type(self,content_type):
        """Convert image type"""

        IMAGE_TYPE = {
            "image/jpeg": 'jpeg',
            "image/png": 'png',
            "image/jpg": 'jpg',
        }

        return IMAGE_TYPE.get(content_type,None)

    async def get_image(self,file_name: str):
        """Get image"""
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image = session.exec(stateman).first()
            session.close()
            return image

    def get_images(self):
        """Get images"""
        with Session(self.engine) as session:
            # query is decrapeated
            stateman = select(Image)
            images = session.exec(stateman).all()
            session.close()
            return images

    async def update_image(self,file_name: str,image: Image):
        """Update image"""
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image: Image | None = session.exec(stateman).first()

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
        """Delete image"""
        with Session(self.engine) as session:
            stateman = select(Image).where(Image.name == file_name)
            image = session.exec(stateman).first()

            if not image:
                return None

            session.delete(image)
            session.commit()
            session.close()
            return image
