
def ResponseModel(data,message):
    return {
        "data":[data],
        "code":200,
        "message":message
    }

def ResponseCreateModel(message):
    return {
        "data": 1,
        "code":201,
        "message":message
    }

def ErrorResponseModel(error,code,message):
    return {
        "error":error,
        "code":code,
        "message":message
    }