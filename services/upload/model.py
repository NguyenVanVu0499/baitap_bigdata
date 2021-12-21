import string
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
import time
from datetime import datetime

class InsertSchema(BaseModel):
    ten_bien_so :str = Field(...)
    # thoi_gian_vao: time
    # thoi_gian_ra: time
    url_img: str = Field(...)
    
    def get_params(self, url_img):

        data = {
            'ten_bien_so': self.ten_bien_so,
            'thoi_gian_vao': int(time.time()),
            'thoi_gian_ra': 0,
            'url_img': url_img,
            'trang_thai': True
        }
        return data