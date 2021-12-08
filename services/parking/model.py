import string
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
import time
from datetime import datetime

class GetSchema(BaseModel):
    ten_bien_so :str = Field(...)
    thoi_gian_vao: time
    thoi_gian_ra: time
    url_img: str = Field(...)
    
    