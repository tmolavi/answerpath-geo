# AnswerPath GEO — موتور استخراج و شبیه‌سازی پرسش‌های هوش مصنوعی (راهنمای فارسی)

[![PyPI version](https://img.shields.io/pypi/v/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![Python versions](https://img.shields.io/pypi/pyversions/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AnswerPath GEO** یک ابزار متن‌باز، بدون وابستگی خارجی و حریم‌خصوصی‌محور برای **کی‌ورد ریسرچ هوش مصنوعی، سئو، GEO (بهینه‌سازی برای موتورهای هوش مصنوعی) و AEO (بهینه‌سازی برای موتورهای پاسخ)** است.

به جای عبارات کلیدواژه‌ای کوتاه، این ابزار سؤالات واقعی و طبیعی را که کاربران از موتورهای هوش مصنوعی (ChatGPT، Perplexity، Claude، Gemini) می‌پرسند استخراج و شبیه‌سازی می‌کند.

---

## قابلیت‌های کلیدی

1. **استخراج هوشمند از آدرس سایت (`--url` یا دادن مستقیم لینک)**:
   - دریافت خودکار متادیتا، نام برند، خدمات اصلی و رقبای وب‌سایت
   - تولید سؤالات مقایسه‌ای و اعتبارسنجی مختص آن برند و وب‌سایت

2. **شبیه‌سازی انواع روش‌های پرسش (Modalities)**:
   - **متنی محاوره‌ای (Conversational Text)**: پرسش‌های چندجمله‌ای واقعی همراه با ذکر دغدغه، بودجه و پیش‌نیازها
   - **صوتی و ویس (Voice Dictation)**: شبیه‌سازی دقیق گفتار و ویس با عبارات محاوره‌ای («سلام چت‌جی‌پی‌تی...»، «ببین من الان...»)
   - **چندحالته و تصویری (Multimodal / Vision)**: ارسال اسکرین‌شات از سایت رقیب، پیش‌فاکتور، نمودار سرچ کنسول یا جدول تعرفه‌ها به همراه متن ارزیابی تصویر

3. **تفکیک پرسونای کاربران و مراحل قیف تصمیم‌گیری**:
   - دسته‌بندی بر اساس پرسونای کاربر (`کارفرما/مدیر کسب‌وکار`، `خریدار فنی`، `مشتری شکاک`، `مدیر مارکتینگ`)
   - دسته‌بندی بر اساس مرحله تصمیم‌گیری (`آگاهی`، `بررسی و مقایسه`، `تصمیم خرید`، `حفظ مشتری`)

4. **سازگاری ۱۰۰٪ با بنچمارک اکوسیستم GEO-Scope**:
   - صدور مستقیم فایل `benchmark_prompts.json` آماده جهت ارزیابی در GEO-Scope

---

## استفاده سریع

```bash
pip install answerpath-geo
```

### ۱. بر اساس موضوع یا کلیدواژه
```bash
answerpath "طراحی سایت فروشگاهی"
```

### ۲. بر اساس آدرس سایت (استخراج خودکار برند و خدمات)
```bash
answerpath https://novin.com --count 30
```

### ۳. فیلتر کردن نوع پرسش (متن، صوت، تصویر)
```bash
# فقط پرسش‌های صوتی و ویس
answerpath "خدمات سئو" --modality voice

# فقط پرسش‌های تصویری با اسکرین‌شات
answerpath "طراحی سایت" --modality image
```

### ۴. استخراج سؤالات واقعی از لاگ‌ها و چت‌های مشتریان
```bash
answerpath "خدمات سئو" --input ./support-logs.json --no-generated
```

---

## خروجی‌ها

دستور خروجی‌ها را در پوشه‌ی `answerpath-output/` ذخیره می‌کند:
- `questions.json`: شامل تمام داده‌های تفصیلی و ساختاریافته
- `questions.csv`: برای باز کردن در اکسل یا گوگل شیت
- `benchmark_prompts.json`: جهت ارزیابی رتبه‌بندی در GEO-Scope

لینک‌ها: [PyPI](https://pypi.org/project/answerpath-geo/) · [GitHub](https://github.com/tmolavi/answerpath-geo) · [Molavi.pro](https://molavi.pro)
