import os
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from supabase import create_client

BOT_TOKEN = os.environ["BOT_TOKEN"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
ADMIN_ID = int(os.environ.get("ADMIN_ID", "0"))
CHANNEL_LINK = "https://t.me/learnin_Everything"
CHANNEL_HANDLE = "@learnin_Everything"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)


class Review(StatesGroup):
    university = State()
    professor = State()
    faculty = State()
    course = State()
    semester = State()
    resources = State()
    attendance = State()
    exam_resources = State()
    grading = State()
    score_continuity = State()
    score_knowledge = State()
    score_responsiveness = State()
    score_communication = State()
    score_management = State()
    contact = State()
    comment = State()
    confirm = State()


def kb(options):
    buttons = [[InlineKeyboardButton(text=o, callback_data=o)] for o in options]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def score_kb():
    buttons = [[InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)],
               [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(6, 11)]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def restart_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔄 ثبت نظر برای استاد دیگر", callback_data="restart")]])


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 سلام! به ربات استادشناسی خوش اومدی.\n\n"
        "این ربات برای جمع‌آوری تجربه‌های واقعی دانشجویان درباره استادها ساخته شده.\n"
        "⚠️ لطفاً اطلاعات را صادقانه وارد کن.\n\n"
        "🎓 اسم دانشگاهت رو بنویس:"
    )
    await state.set_state(Review.university)


@router.message(Review.university)
async def get_university(message: Message, state: FSMContext):
    await state.update_data(university=message.text)
    await message.answer("🧑‍🏫 نام و نام خانوادگی استاد را وارد کن:")
    await state.set_state(Review.professor)


@router.message(Review.professor)
async def get_professor(message: Message, state: FSMContext):
    await state.update_data(professor=message.text)
    await message.answer(
        "📚 نام دانشکده‌ای که در آن هستید چیست؟",
        reply_markup=kb(["پزشکی", "دندانپزشکی", "داروسازی", "پرستاری", "مامایی", "بهداشت", "پیراپزشکی", "➕ سایر"])
    )
    await state.set_state(Review.faculty)


@router.callback_query(Review.faculty)
async def get_faculty(call: CallbackQuery, state: FSMContext):
    if call.data == "➕ سایر":
        await call.message.answer("✏️ نام دانشکده رو بنویس:")
        await call.answer()
        return
    await state.update_data(faculty=call.data)
    await call.message.answer("📖 نام درسی که با این استاد داشتی رو بنویس:")
    await state.set_state(Review.course)
    await call.answer()


@router.message(Review.faculty)
async def get_faculty_custom(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer("📖 نام درسی که با این استاد داشتی رو بنویس:")
    await state.set_state(Review.course)


@router.message(Review.course)
async def get_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer(
        "🗓️ در چه ترمی با این استاد کلاس داشتی؟",
        reply_markup=kb(["ترم ۱", "ترم ۲", "ترم ۳", "ترم ۴", "ترم ۵", "ترم ۶",
                          "ترم ۷", "ترم ۸", "ترم ۹", "ترم ۱۰", "ترم ۱۱", "ترم ۱۲", "➕ سایر"])
    )
    await state.set_state(Review.semester)


@router.callback_query(Review.semester)
async def get_semester(call: CallbackQuery, state: FSMContext):
    if call.data == "➕ سایر":
        await call.message.answer("✏️ ترم رو بنویس:")
        await call.answer()
        return
    await state.update_data(semester=call.data)
    await call.message.answer(
        "📚 استاد برای تدریس از چه منابعی استفاده می‌کرد؟",
        reply_markup=kb(["جزوه", "PowerPoint/PDF", "کتاب مرجع", "جزوه‌نویسی در کلاس", "ویدیوی آموزشی", "منبع مشخصی معرفی نمی‌کند"])
    )
    await state.set_state(Review.resources)
    await call.answer()


@router.message(Review.semester)
async def get_semester_custom(message: Message, state: FSMContext):
    await state.update_data(semester=message.text)
    await message.answer(
        "📚 استاد برای تدریس از چه منابعی استفاده می‌کرد؟",
        reply_markup=kb(["جزوه", "PowerPoint/PDF", "کتاب مرجع", "جزوه‌نویسی در کلاس", "ویدیوی آموزشی", "منبع مشخصی معرفی نمی‌کند"])
    )
    await state.set_state(Review.resources)


@router.callback_query(Review.resources)
async def get_resources(call: CallbackQuery, state: FSMContext):
    await state.update_data(resources=call.data)
    await call.message.answer(
        "✅ وضعیت حضور و غیاب استاد چطور بود؟",
        reply_markup=kb(["حضور خیلی مهم است", "حضور مهم است", "تأثیر مثبت دارد", "حضور مهم نیست", "حضور و غیاب ندارد"])
    )
    await state.set_state(Review.attendance)
    await call.answer()


@router.callback_query(Review.attendance)
async def get_attendance(call: CallbackQuery, state: FSMContext):
    await state.update_data(attendance=call.data)
    await call.message.answer(
        "📝 آیا منابعی که استاد معرفی کرده برای امتحان کافی بود؟",
        reply_markup=kb(["بله کاملاً", "تا حدودی", "خیر"])
    )
    await state.set_state(Review.exam_resources)
    await call.answer()


@router.callback_query(Review.exam_resources)
async def get_exam_resources(call: CallbackQuery, state: FSMContext):
    await state.update_data(exam_resources=call.data)
    await call.message.answer(
        "⭐ وضعیت نمره‌دهی استاد چطور بود؟",
        reply_markup=kb(["خیلی دست‌باز", "دست‌باز و با ارفاق", "منصفانه", "سخت‌گیر", "خیلی سخت‌گیر"])
    )
    await state.set_state(Review.grading)
    await call.answer()


@router.callback_query(Review.grading)
async def get_grading(call: CallbackQuery, state: FSMContext):
    await state.update_data(grading=call.data)
    await call.message.answer("📊 پیوستگی و یکپارچگی تدریس رو از ۱ تا ۱۰ نمره بده:", reply_markup=score_kb())
    await state.set_state(Review.score_continuity)
    await call.answer()


@router.callback_query(Review.score_continuity)
async def score_continuity(call: CallbackQuery, state: FSMContext):
    await state.update_data(teaching_continuity=int(call.data))
    await call.message.answer("🧠 دانش عمومی و تسلط استاد رو از ۱ تا ۱۰ نمره بده:", reply_markup=score_kb())
    await state.set_state(Review.score_knowledge)
    await call.answer()


@router.callback_query(Review.score_knowledge)
async def score_knowledge(call: CallbackQuery, state: FSMContext):
    await state.update_data(knowledge=int(call.data))
    await call.message.answer("💬 پاسخگویی استاد رو از ۱ تا ۱۰ نمره بده:", reply_markup=score_kb())
    await state.set_state(Review.score_responsiveness)
    await call.answer()


@router.callback_query(Review.score_responsiveness)
async def score_responsiveness(call: CallbackQuery, state: FSMContext):
    await state.update_data(responsiveness=int(call.data))
    await call.message.answer("📢 توانایی انتقال مطالب رو از ۱ تا ۱۰ نمره بده:", reply_markup=score_kb())
    await state.set_state(Review.score_communication)
    await call.answer()


@router.callback_query(Review.score_communication)
async def score_communication(call: CallbackQuery, state: FSMContext):
    await state.update_data(communication=int(call.data))
    await call.message.answer("⏰ نظم و مدیریت کلاس رو از ۱ تا ۱۰ نمره بده:", reply_markup=score_kb())
    await state.set_state(Review.score_management)
    await call.answer()


@router.callback_query(Review.score_management)
async def score_management(call: CallbackQuery, state: FSMContext):
    await state.update_data(class_management=int(call.data))
    await call.message.answer(
        "📲 استاد از چه راهی با دانشجویان ارتباط داشت؟",
        reply_markup=kb(["تلگرام", "واتساپ", "ایتا", "گروه درسی", "راه ارتباطی مشخصی ندارد"])
    )
    await state.set_state(Review.contact)
    await call.answer()


@router.callback_query(Review.contact)
async def get_contact(call: CallbackQuery, state: FSMContext):
    await state.update_data(contact_methods=call.data)
    await call.message.answer(
        "✍️ تجربه‌ات از این استاد رو بنویس (نحوه تدریس، رفتار، امتحان و هر نکته‌ی مفید دیگه).\n"
        "⚠️ لطفاً از توهین و اطلاعات شخصی خودداری کن."
    )
    await state.set_state(Review.comment)
    await call.answer()


@router.message(Review.comment)
async def get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()

    summary = (
        f"👀 اطلاعات ثبت‌شده:\n\n"
        f"🎓 دانشگاه: {data['university']}\n"
        f"🧑‍🏫 استاد: {data['professor']}\n"
        f"📚 دانشکده: {data['faculty']}\n"
        f"📖 درس: {data['course']}\n"
        f"🗓️ ترم: {data['semester']}\n"
        f"📚 منابع: {data['resources']}\n"
        f"✅ حضور و غیاب: {data['attendance']}\n"
        f"📝 منابع امتحان: {data['exam_resources']}\n"
        f"⭐ نمره‌دهی: {data['grading']}\n"
        f"📊 پیوستگی: {data['teaching_continuity']}/10\n"
        f"🧠 تسلط: {data['knowledge']}/10\n"
        f"💬 پاسخگویی: {data['responsiveness']}/10\n"
        f"📢 انتقال مطلب: {data['communication']}/10\n"
        f"⏰ مدیریت کلاس: {data['class_management']}/10\n"
        f"📲 ارتباط: {data['contact_methods']}\n"
        f"✍️ توضیحات: {data['comment']}\n"
    )
    await message.answer(summary, reply_markup=kb(["✅ ثبت نهایی", "❌ لغو"]))
    await state.set_state(Review.confirm)


@router.callback_query(Review.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if call.data == "✅ ثبت نهایی":
        uni = supabase.table("universities").upsert({"name": data["university"]}, on_conflict="name").execute()
        uni_id = uni.data[0]["id"] if uni.data else supabase.table("universities").select("id").eq("name", data["university"]).execute().data[0]["id"]

        prof = supabase.table("professors").insert({
            "university_id": uni_id,
            "name": data["professor"],
            "faculty": data["faculty"],
        }).execute()
        prof_id = prof.data[0]["id"]

        course = supabase.table("courses").insert({
            "professor_id": prof_id,
            "name": data["course"],
        }).execute()
        course_id = course.data[0]["id"]

        supabase.table("reviews").insert({
            "professor_id": prof_id,
            "course_id": course_id,
            "semester": data["semester"],
            "resources": data["resources"],
            "attendance": data["attendance"],
            "exam_resources": data["exam_resources"],
            "grading": data["grading"],
            "teaching_continuity": data["teaching_continuity"],
            "knowledge": data["knowledge"],
            "responsiveness": data["responsiveness"],
            "communication": data["communication"],
            "class_management": data["class_management"],
            "contact_methods": data["contact_methods"],
            "comment": data["comment"],
            "telegram_user_id": call.from_user.id,
            "status": "pending",
        }).execute()

        final_text = (
            "🎉 <b>ممنون بابت نظر ارزشمندت!</b>\n"
            "نظرت با موفقیت ثبت شد ✅\n\n"
            "📌 <u>نکته مهم:</u> وقتی نظرات کافی برای این استاد جمع بشه، همه‌شون رو "
            "<b>یکجا جمع‌بندی می‌کنیم</b> و به‌صورت یک پست کامل توی کانال منتشر می‌کنیم "
            "تا بقیه‌ی دانشجوها هم از تجربه‌ی شما استفاده کنن 📊🙌\n\n"
            f"📢 برای دیدن نتایج و آمار استادها، عضو کانال شو:\n"
            f'👉 <a href="{CHANNEL_LINK}">{CHANNEL_HANDLE}</a>'
        )
        await call.message.answer(final_text, reply_markup=restart_kb(), parse_mode="HTML", disable_web_page_preview=True)

        if ADMIN_ID:
            await bot.send_message(ADMIN_ID, f"🔔 نظر جدید ثبت شد:\n\n{data['professor']} - {data['course']}")
    else:
        await call.message.answer(
            "❌ <b>لغو شد.</b>\nبرای شروع دوباره روی دکمه‌ی زیر بزن 🔄",
            reply_markup=restart_kb(),
            parse_mode="HTML"
        )

    await state.clear()
    await call.answer()


@router.callback_query(F.data == "restart")
async def restart(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("🎓 اسم دانشگاهت رو بنویس:")
    await state.set_state(Review.university)
    await call.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
