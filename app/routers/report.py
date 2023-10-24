from fastapi import FastAPI,  APIRouter

router = APIRouter()

@router.get("/get_reports")
async def get_data():
    return {}
    # conn = get_database_connection()
    # with conn.cursor() as cursor:
    #     cursor.execute("SELECT * FROM report")
    #     data = cursor.fetchall()
    # conn.close()
    # return data