import os
from dotenv import load_dotenv
import sys
import django
from datetime import datetime
import pytz  # ✅ For Bangladesh timezone

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from asgiref.sync import sync_to_async



# ✅ Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_project.settings')
django.setup()

from attendance_app.models import Employee, Attendance

# ✅ Constants
load_dotenv()  # Load variables from .env

BOT_TOKEN = os.getenv('BOT_TOKEN')
BD_TZ = pytz.timezone("Asia/Dhaka")  # ✅ Bangladesh Timezone

# ✅ Format functions with proper timezone conversion
def format_time(dt):
    local_dt = dt.astimezone(BD_TZ)
    return local_dt.strftime("%I:%M %p")

def format_full_date(dt):
    local_dt = dt.astimezone(BD_TZ)
    return local_dt.strftime("%A %B %d %Y %I:%M:%S %p")

# ✅ Database operations wrapped in sync_to_async
@sync_to_async
def get_or_create_employee(user_id, name):
    return Employee.objects.get_or_create(
        telegram_user_id=user_id,
        defaults={'full_name': name}
    )

@sync_to_async
def get_attendance_for_date(employee, date):
    return Attendance.objects.filter(employee=employee, date=date).first()

@sync_to_async
def create_attendance(employee, date, now):
    return Attendance.objects.create(employee=employee, date=date, check_in=now)

@sync_to_async
def update_check_out(attendance, now):
    attendance.check_out = now
    attendance.save()

@sync_to_async
def update_check_in(attendance, now):
    attendance.check_in = now
    attendance.save()

# ✅ Main handler
async def handle_checkin_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_message = update.message.text.strip().lower()
    user = update.message.from_user
    user_id = user.id
    name = user.full_name

    now = datetime.now(BD_TZ)  # ✅ Current time in BD
    today = now.date()

    employee, _ = await get_or_create_employee(user_id, name)
    attendance = await get_attendance_for_date(employee, today)

    if user_message == 'hi':
        if attendance and attendance.check_in:
            await update.message.reply_text(
                f"✅ You've already checked in today at {format_time(attendance.check_in)}, {name}."
            )
        else:
            if not attendance:
                await create_attendance(employee, today, now)
            else:
                await update_check_in(attendance, now)

            await update.message.reply_text(
                f"Hi! 👋 {name}, it's {format_full_date(now)}.\nYour check-in has been recorded."
            )

    elif user_message == 'bye':
        if not attendance or not attendance.check_in:
            await update.message.reply_text(f"❌ You haven't checked in yet today, {name}.")
            return

        if attendance.check_out:
            await update.message.reply_text(
                f"✅ You've already checked out today at {format_time(attendance.check_out)}, {name}."
            )
            return

        await update_check_out(attendance, now)
        duration = attendance.total_duration()
        hours, remainder = divmod(duration.seconds, 3600)
        minutes = remainder // 60

        await update.message.reply_text(
            f"👋 Bye, {name}!\n"
            f"🕗 Checked in at {format_time(attendance.check_in)}.\n"
            f"🕖 Checked out at {format_time(attendance.check_out)}.\n"
            f"⌛ Total time today is {hours:02d} hours {minutes:02d} mins."
        )

# ✅ App entry point
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_checkin_checkout)
    app.add_handler(message_handler)
    app.run_polling()
