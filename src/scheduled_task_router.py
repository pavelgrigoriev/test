# scheduled_task_router.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, BackgroundTasks
import asyncio

from router_mysql import send_statistics_email
from router_sqlite import get_user_by_id, get_db
from send_email import EmailSchema

router = APIRouter()
scheduler = AsyncIOScheduler()


async def send_statistics_email_task():
    db = next(get_db())  # Get database session
    user = get_user_by_id(0, db=db)  # Pass the database session to get_user_by_id
    serialized_user = serialize_user(user)  # Convert User object to JSON-serializable format
    if serialized_user["mail_enabled"] == True:
        destination_email = serialized_user["destination_email"]
        email_schema = EmailSchema(email=[destination_email])
        await send_statistics_email(email=email_schema)


def serialize_user(user):
    return {
        'mail_enabled': user.mail_enabled,
        'destination_email': user.destination_email,
        'id': user.id
    }


@router.post("/schedule_task")
async def schedule_task(background_tasks: BackgroundTasks):
    # Schedule the task to run on the 1st day of each month at 00:00
    scheduler.add_job(send_statistics_email_task, 'interval', seconds=10)
    # Start the scheduler
    scheduler.start()
    return {"message": "Task scheduled"}


@router.post("/stop_task")
async def stop_task():
    # Stop the scheduler
    scheduler.shutdown()
    return {"message": "Task stopped"}


# Add route to manually trigger the task for testing purposes
@router.post("/trigger_task")
async def trigger_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_statistics_email_task)
    return {"message": "Task triggered"}


# Stop the scheduler when the app shuts down
@router.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


async def send_email_periodically(email: EmailSchema, interval: int):
    while True:
        await asyncio.sleep(interval)
        await send_statistics_email(email)
        

@router.post("/schedule-email")
async def schedule_email(background_tasks: BackgroundTasks, email: EmailSchema, interval: int):
    background_tasks.add_task(send_email_periodically, email, interval)
    return {"message": f"Email will be sent to {email.email} every {interval} seconds."}