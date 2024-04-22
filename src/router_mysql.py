import tempfile
from fastapi import APIRouter
from mysql import connect_to_mysql
import datetime
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from send_email import EmailSchema, conf
from async_lru import alru_cache
from uttils import prepare_to_csv

router = APIRouter(
    prefix="/getdata"
)

@alru_cache
@router.get("")
async def get_statistics():
    connection = await connect_to_mysql()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM `Statistic_material`"
        await cursor.execute(query)
        statistics = await cursor.fetchall()
    connection.close()
    return {"statistics": statistics}

@alru_cache
@router.get("/{datetime}")
async def get_statistics_by_hour(datetime: datetime.datetime):
    connection = await connect_to_mysql()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM `Statistic_material` WHERE DataTime = %s"
        await cursor.execute(query, (datetime,))
        statistics = await cursor.fetchall()
    connection.close()
    return {"statistics": statistics}

@alru_cache
@router.get("/range/")
async def get_statistics_by_range(start_datetime: datetime.datetime, end_datetime: datetime.datetime):
    connection = await connect_to_mysql()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM `Statistic_material` WHERE DataTime BETWEEN %s AND %s"
        await cursor.execute(query, (start_datetime, end_datetime))
        statistics = await cursor.fetchall()
    connection.close()
    return {"statistics": statistics}

@router.post("/sendfile")
async def send_statistics_email(email: EmailSchema) -> JSONResponse:
    # Fetch statistics from the database
    connection = await connect_to_mysql()
    async with connection.cursor() as cursor:
        query = "SELECT * FROM `Statistic_material`"
        await cursor.execute(query)
        statistics = await cursor.fetchall()
    connection.close()

    csv_data = prepare_to_csv(statistics)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as temp_file:
        temp_file.write(csv_data.getvalue())

    # Prepare email message
    message = MessageSchema(
        subject="Statistics Data",
        recipients=email.dict().get("email"),
        body="Please find attached the aggregated statistics data.",
        subtype=MessageType.html,
        attachments=[temp_file.name],  # Pass the path of the temporary file
    )

    # Send email
    fm = FastMail(conf)
    await fm.send_message(message)

    # Delete the temporary file
    temp_file.close()
    return JSONResponse(status_code=200, content={"message": "Email has been sent with the statistics data."})


