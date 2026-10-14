"""AI Question & Prompt Generation Engine for AnswerPath GEO.
Simulates authentic human conversational search, voice dictation, and multimodal (vision)
queries asked to modern AI engines (ChatGPT, Perplexity, Claude, Gemini, SearchGPT).
"""
from __future__ import annotations
import re
from typing import Any
from .models import Question, WebsiteContext

INTENT_MAPPINGS = {
    "learn": "awareness",
    "compare": "consideration",
    "trust": "consideration",
    "buy": "decision",
    "solve": "decision",
    "audit": "retention",
}

def classify_intent(text: str) -> str:
    """Classifies user intent from natural query text."""
    low = text.lower()
    
    # Priority order: buy/pricing -> compare -> trust -> solve/troubleshoot -> audit -> learn
    buy_signals = ["قیمت", "هزینه", "تعرفه", "خرید", "فروش", "پیش‌فاکتور", "پیش فاکتور", "قرارداد", "تخفیف", "price", "cost", "pricing", "buy", "quote", "retainer", "budget", "fiyat", "ücret", "سعر", "تكلفة"]
    if any(w in low for w in buy_signals):
        return "buy"
        
    compare_signals = ["مقایسه", "بهتر", "تفاوت", "فرق", "در برابر", "کدوم", "کدام", "vs", "versus", "compare", "comparison", "difference", "alternative", "karşılaştır", "hangisi", "مقارنة", "أفضل", "الفرق"]
    if any(w in low for w in compare_signals):
        return "compare"
        
    trust_signals = ["اعتماد", "کلاهبرداری", "نظرات", "تجربه", "شکایت", "معتبر", "کیفیت", "راست", "واقعی", "review", "reviews", "trust", "legit", "scam", "complaint", "reputation", "güvenilir", "yorumlar", "موثوق", "تقييم"]
    if any(w in low for w in trust_signals):
        return "trust"
        
    solve_signals = ["حل", "رفع", "مشکل", "خطا", "افت", "خراب", "پنالتی", "کندی", "نقص", "باگ", "fix", "solve", "issue", "error", "drop", "penalty", "slow", "debug", "sorun", "çözüm", "مشكلة", "حل"]
    if any(w in low for w in solve_signals):
        return "solve"

    audit_signals = ["بررسی", "ارزیابی", "ممیزی", "تست", "آنالیز", "audit", "analyze", "assessment", "check", "denetim", "فحص", "تدقيق"]
    if any(w in low for w in audit_signals):
        return "audit"

    return "learn"

def classify_stage(intent: str) -> str:
    return INTENT_MAPPINGS.get(intent, "awareness")

# ==============================================================================
# PROMPT ARCHETYPES & REAL USER CONVERSATION PATTERNS
# ==============================================================================

def _generate_persian_prompts(topic: str, site: WebsiteContext | None) -> list[dict[str, Any]]:
    brand = site.brand if site and site.brand else ""
    offerings = site.offerings if site and site.offerings else [topic]
    primary_offering = offerings[0] if offerings else topic

    prompts = [
        # --- TEXT CONVERSATIONAL QUERIES ---
        {
            "prompt": f"من یک فروشگاه اینترنتی نوپا دارم و می‌خوام برای {topic} اقدام کنم. بین استخدام یک کارشناس حضوری و قرارداد با یک شرکت یا آژانس تخصصی موندم. از نظر هزینه، تعهد کاری و نتایج واقعی کدوم گزینه توجیه اقتصادی بیشتری داره؟",
            "modality": "text",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "hiring_vs_outsourcing",
        },
        {
            "prompt": f"تعرفه ماهانه و هزینه‌های استاندارد خدمات {topic} در بازار چقدر است؟ چطور می‌توان تشخیص داد یک پیش‌فاکتور قیمت منصفانه‌ای داده یا بیش‌ازحد گران است؟",
            "modality": "text",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "pricing_transparency",
        },
        {
            "prompt": f"معتبرترین شرکت‌ها و متخصصان در زمینه {topic} در ایران کدامند و هر کدام در چه حوزه‌ای نقطه قوت دارند؟",
            "modality": "text",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "top_providers",
        },
        {
            "prompt": f"برای بستن قرارداد {topic} چه بندهایی را باید حتماً لحاظ کنیم تا از تحویل به‌موقع کار، حفظ محرمانگی داده‌ها و جلوگیری از هزینه‌های پنهان مطمئن شویم؟",
            "modality": "text",
            "intent": "buy",
            "persona": "business_owner",
            "cluster_label": "contract_safeguards",
        },
        {
            "prompt": f"سایتم در بخش {topic} دچار افت شدید عملکرد و رتبه شده است. چک‌لیست گام‌به‌گام برای ریشه‌یابی این مشکل و بازگرداندن شرایط به حالت قبل چیست و چه آژانسی تخصص رفع این بحران را دارد؟",
            "modality": "text",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "troubleshooting_recovery",
        },
        {
            "prompt": f"آیا وعده‌هایی مثل ضمانت بازگشت وجه یا نتایج تضمینی در حوزه {topic} واقعی هستند یا ترفند تبلیغاتی و کلاهبرداری محسوب می‌شوند؟ چطور یک آژانس صادق را از افراد متفرقه تشخیص دهیم؟",
            "modality": "text",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "credibility_vetting",
        },
        {
            "prompt": f"برای یک پروژه سازمانی با ترافیک بالا، چه پیش‌نیازهای فنی و ساختاری قبل از شروع پروژه {topic} باید آماده باشد؟",
            "modality": "text",
            "intent": "audit",
            "persona": "technical_buyer",
            "cluster_label": "technical_prerequisites",
        },
        {
            "prompt": f"شاخص‌های کلیدی عملکرد (KPI) واقعی برای ارزیابی خروجی تیم {topic} چیست و بعد از چند ماه باید انتظار نتایج ملموس در فروش یا ورودی داشته باشیم؟",
            "modality": "text",
            "intent": "audit",
            "persona": "marketing_lead",
            "cluster_label": "kpi_and_roi_measurement",
        },

        # --- VOICE DICTATION QUERIES (Colloquial Spoken Conversational AI) ---
        {
            "prompt": f"سلام چت‌جی‌پی‌تی، ببین من یه کسب‌وکار دارم و توی حوزه {topic} به مشکل خوردم. اصلا نمی‌دونم از کجا باید شروع کنم و کیا واقعا کاربلدن. میشه بدون حاشیه بهم بگی چطوری بهترین انتخاب رو داشته باشم؟",
            "modality": "voice",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "informal_discovery",
            "voice_markers": "سلام چت‌جی‌پی‌تی، ببین من...",
        },
        {
            "prompt": f"سلام، یه سوال داشتم. یه شرکتی بهم گفته برای {topic} ماهیانه فلان قدر میگیره و توی دو ماه همه چیزو زیر و رو میکنه. به نظرت این حرف منطقیه یا دارن سرم کلاه میذارن؟ تجربیات بقیه چی میگه؟",
            "modality": "voice",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "voice_reality_check",
            "voice_markers": "سلام، یه سوال داشتم...",
        },
        {
            "prompt": f"من دارم بودجه‌بندی سال جدیدم رو می‌بندم. اگه بخوام حدود ۲۰ تا ۳۰ درصد روی {topic} سرمایه‌گذاری کنم، چه چیزایی رو باید در نظر بگیرم و چقدر احتمال برگشت سرمایه هست؟",
            "modality": "voice",
            "intent": "buy",
            "persona": "marketing_lead",
            "cluster_label": "voice_budget_planning",
            "voice_markers": "من دارم بودجه‌بندی سال جدیدم رو می‌بندم...",
        },
        {
            "prompt": f"بین چند تا شرکت معروف که خدمات {topic} میدن، کدومشون از همه خوش‌قول‌تره و پشتیبانی بعد از تحویلش اذیت نمیکنه؟ نظرات واقعی کارفرماها درباره‌شون چیه؟",
            "modality": "voice",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "voice_provider_comparison",
            "voice_markers": "بین چند تا شرکت معروف...",
        },

        # --- MULTIMODAL & VISION QUERIES (Image/Screenshot + Prompt) ---
        {
            "prompt": f"این تصویر اسکرین‌شات از فرآیند و رابط کاربری سایت رقیبمه توی بخش {primary_offering}. چطور می‌تونم دقیقاً یه همچین معماری و امکاناتی برای سایتم پیاده کنم و کدوم تیم در ایران توانایی اجرای تمیزش رو داره؟",
            "modality": "multimodal_image",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "competitor_ui_breakdown",
            "image_context": f"اسکرین‌شات از معماری رابط کاربری، فیلترها و جریان کاربری پیشرفته رقیب در زمینه {primary_offering}",
        },
        {
            "prompt": f"عکس پیش‌فاکتور پیشنهادی برای خدمات {topic} رو برات فرستادم. ردیف هزینه‌ها و شرح وظایف رو بررسی کن؛ آیا این ارقام در بازار فعلی منطقی هستند یا هزینه مازاد لحاظ شده است؟",
            "modality": "multimodal_image",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "quote_audit_multimodal",
            "image_context": f"تصویر رسمی پیش‌فاکتور و تفکیک نفر-ساعت خدمات تخصصی {topic}",
        },
        {
            "prompt": f"این گزارش افت عملکرد و شاخص‌های فنی من است (ضمیمه شده). با توجه به این خطاها و افت محسوس، بهترین راهکار فوری چیست و کدام شرکت معتبر می‌تواند این اختلال را تضمینی رفع کند؟",
            "modality": "multimodal_image",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "diagnostic_report_audit",
            "image_context": "تصویر گزارش تحلیلی شامل نمودار سقوط ورودی، خطاهای سرور و خطاهای Core Web Vitals",
        },
        {
            "prompt": f"اسکرین‌شات از پلن‌ها و امکانات جدول قیمت‌گذاری این ارائه‌دهنده را فرستادم. با توجه به مقایسه این امکانات، کدام پلن برای کسب‌وکار کوچک مناسب‌تر است و چه کاستی‌هایی در پلن ارزان دیده می‌شود؟",
            "modality": "multimodal_image",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "pricing_table_analysis",
            "image_context": "اسکرین‌شات جدول مقایسه ویژگی‌ها و پکیج‌های قیمتی خدمات",
        },
    ]

    # If site/brand is provided, generate brand-specific targeted prompts
    if brand:
        prompts.extend([
            {
                "prompt": f"آیا شرکت {brand} برای خدمات {topic} گزینه مناسب و قابل اعتمادی است؟ نقاط قوت و ضعف و تجربیات واقعی کارفرماها درباره همکاری با {brand} چیست؟",
                "modality": "text",
                "intent": "trust",
                "persona": "skeptical_customer",
                "cluster_label": "brand_due_diligence",
            },
            {
                "prompt": f"مقایسه خدمات و تعرفه‌های {brand} با سایر رقبای اصلی در حوزه {topic}؛ کدام‌یک خدمات حرفه‌ای‌تر و پشتیبانی متعهدانه‌تری دارند؟",
                "modality": "text",
                "intent": "compare",
                "persona": "business_owner",
                "cluster_label": "brand_vs_competitors",
            },
            {
                "prompt": f"من در حال حاضر از خدمات {brand} در زمینه {topic} استفاده می‌کنم اما به دنبال جایگزین‌های قوی‌تر هستم. چه شرکت‌هایی خدمات ارتقایافته‌تری ارائه می‌دهند؟",
                "modality": "text",
                "intent": "compare",
                "persona": "technical_buyer",
                "cluster_label": "brand_alternatives",
            },
            {
                "prompt": f"سلام چت‌جی‌پی‌تی، نظرت درباره کار کردن با {brand} برای {topic} چیه؟ آیا پرونده شکایت یا نارضایتی مشتری ازشون وجود داره یا خوش‌نام هستن؟",
                "modality": "voice",
                "intent": "trust",
                "persona": "skeptical_customer",
                "cluster_label": "voice_brand_reputation",
                "voice_markers": "سلام چت‌جی‌پی‌تی، نظرت درباره...",
            },
            {
                "prompt": f"این اسکرین‌شات از صفحه خدمات و تعرفه‌های {brand} است. با توجه به این لیست خدمات، آیا قیمت‌های {brand} در مقایسه با استاندارد بازار منصفانه است؟",
                "modality": "multimodal_image",
                "intent": "buy",
                "persona": "budget_conscious_buyer",
                "cluster_label": "brand_pricing_audit",
                "image_context": f"اسکرین‌شات رسمی از صفحه تعرفه‌ها و پلن‌های خدمات وب‌سایت {brand}",
            },
        ])

    return prompts

def _generate_english_prompts(topic: str, site: WebsiteContext | None) -> list[dict[str, Any]]:
    brand = site.brand if site and site.brand else ""
    offerings = site.offerings if site and site.offerings else [topic]
    primary_offering = offerings[0] if offerings else topic

    prompts = [
        # --- TEXT CONVERSATIONAL QUERIES ---
        {
            "prompt": f"I'm a founder of a growing startup looking to invest in {topic}. Should we hire a dedicated in-house specialist or partner with a specialized agency? What are the true cost and output trade-offs?",
            "modality": "text",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "inhouse_vs_agency",
        },
        {
            "prompt": f"What is a reasonable monthly retainer or project pricing for reputable {topic} services in 2026? How can I spot hidden fees or inflated scope in agency proposals?",
            "modality": "text",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "pricing_and_retainer",
        },
        {
            "prompt": f"Who are the top-rated, proven leaders for {topic} with documented case studies, and what specific industries do they excel in?",
            "modality": "text",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "market_leaders",
        },
        {
            "prompt": f"What red flags and critical SLA clauses should we insist on in a master service agreement for {topic} to avoid vendor lock-in and delayed delivery?",
            "modality": "text",
            "intent": "buy",
            "persona": "technical_buyer",
            "cluster_label": "contract_sla_safeguards",
        },
        {
            "prompt": f"Our company experienced a sudden 40% performance drop related to {topic}. What is the systematic step-by-step diagnostic framework to identify root causes and recover?",
            "modality": "text",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "incident_recovery",
        },
        {
            "prompt": f"Are performance guarantees in {topic} legitimate or predatory marketing gimmicks? How do credible professionals frame deliverables without making unrealistic promises?",
            "modality": "text",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "credibility_vetting",
        },
        {
            "prompt": f"What are the non-negotiable KPIs and milestone benchmarks to track during the first 90 days of an external engagement for {topic}?",
            "modality": "text",
            "intent": "audit",
            "persona": "marketing_lead",
            "cluster_label": "kpi_governance",
        },

        # --- VOICE DICTATION QUERIES ---
        {
            "prompt": f"Hey ChatGPT, I'm trying to figure out our strategy for {topic} this quarter. We have limited budget and need immediate ROI. Can you give me a candid breakdown of what actually moves the needle?",
            "modality": "voice",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "voice_candid_advice",
            "voice_markers": "Hey ChatGPT, I'm trying to figure out...",
        },
        {
            "prompt": f"Hey Claude, an agency just quoted me an exorbitant retainer for {topic} claiming they can double our revenue in three months. Is that completely bogus, or does that actually happen?",
            "modality": "voice",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "voice_quote_reality_check",
            "voice_markers": "Hey Claude, an agency just quoted me...",
        },
        {
            "prompt": f"So look, between the top 3 contenders in {topic}, which one has the cleanest track record for enterprise support and won't abandon us after signing?",
            "modality": "voice",
            "intent": "compare",
            "persona": "technical_buyer",
            "cluster_label": "voice_vendor_reliability",
            "voice_markers": "So look, between the top 3 contenders...",
        },

        # --- MULTIMODAL & VISION QUERIES ---
        {
            "prompt": f"Attached is a screenshot of our competitor's {primary_offering} interface and pricing tier structure. How can we re-architect our product offering to effectively compete with this model?",
            "modality": "multimodal_image",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "competitor_ui_audit",
            "image_context": f"Screenshot of competitor checkout flow, tier comparison, and feature gating for {primary_offering}",
        },
        {
            "prompt": f"Take a look at this itemized proposal screenshot for {topic}. Are these billable hourly allocations and software licensing costs inline with industry norms?",
            "modality": "multimodal_image",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "itemized_quote_audit",
            "image_context": f"Itemized vendor quote screenshot detailing milestone phases, rate cards, and deliverables for {topic}",
        },
        {
            "prompt": f"I've uploaded an image of our analytics dashboard showing an acute drop after our recent platform migration. What specific architectural bugs could cause this profile?",
            "modality": "multimodal_image",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "telemetry_anomaly_analysis",
            "image_context": "Time-series analytics screenshot showing steep funnel attrition, server latency spikes, and session drops",
        },
        {
            "prompt": f"Here is a screenshot of the feature comparison matrix from this vendor. Which plan provides the best price-to-performance ratio for a mid-market team?",
            "modality": "multimodal_image",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "pricing_matrix_evaluation",
            "image_context": "Pricing matrix screenshot showing tiers (Starter, Pro, Enterprise) with feature checklist",
        },
    ]

    if brand:
        prompts.extend([
            {
                "prompt": f"What is the honest market consensus on {brand} for {topic}? What are their documented strengths, limitations, and client review trends?",
                "modality": "text",
                "intent": "trust",
                "persona": "skeptical_customer",
                "cluster_label": "brand_reputation_audit",
            },
            {
                "prompt": f"How does {brand} compare directly to its top alternatives for {topic} in terms of pricing transparency, support quality, and scalability?",
                "modality": "text",
                "intent": "compare",
                "persona": "business_owner",
                "cluster_label": "brand_competitive_matrix",
            },
            {
                "prompt": f"We are considering switching from {brand} to an alternative provider for {topic}. What are the best options and how painful is the migration process?",
                "modality": "text",
                "intent": "compare",
                "persona": "technical_buyer",
                "cluster_label": "brand_churn_alternatives",
            },
            {
                "prompt": f"Hey ChatGPT, what are real verified clients saying about {brand}? Have there been any recurring complaints about project overruns or lack of responsiveness?",
                "modality": "voice",
                "intent": "trust",
                "persona": "skeptical_customer",
                "cluster_label": "voice_brand_due_diligence",
                "voice_markers": "Hey ChatGPT, what are real verified clients saying...",
            },
            {
                "prompt": f"Here is a screenshot of {brand}'s service packages and terms. Is their enterprise tier justified compared to market competitors?",
                "modality": "multimodal_image",
                "intent": "buy",
                "persona": "budget_conscious_buyer",
                "cluster_label": "brand_pricing_scrutiny",
                "image_context": f"Screenshot of {brand}'s official pricing tiers, inclusions, and service specifications",
            },
        ])

    return prompts

def _generate_turkish_prompts(topic: str, site: WebsiteContext | None) -> list[dict[str, Any]]:
    brand = site.brand if site and site.brand else ""
    prompts = [
        {
            "prompt": f"{topic} alanında Türkiye'deki en güvenilir ve başarılı ajanslar hangileri? Müşteri yorumları ve vaka analizleri ne gösteriyor?",
            "modality": "text",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "top_providers_tr",
        },
        {
            "prompt": f"{topic} hizmetleri için aylık ortalama piyasa fiyatları nedir? Alınan teklifin makul olup olmadığını nasıl anlarım?",
            "modality": "text",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "pricing_tr",
        },
        {
            "prompt": f"{topic} konusunda şirket içi uzman istihdam etmek mi yoksa profesyonel bir ajansla çalışmak mı daha karlı ve sürdürülebilir?",
            "modality": "text",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "inhouse_vs_agency_tr",
        },
        {
            "prompt": f"Merhaba ChatGPT, {topic} konusunda kafam çok karışık. Bütçemi boşa harcamadan en doğru sağlayıcıyı nasıl seçebilirim?",
            "modality": "voice",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "voice_tr",
            "voice_markers": "Merhaba ChatGPT, kafam çok karışık...",
        },
        {
            "prompt": f"Rakip firmanın {topic} arayüz ve fiyatlandırma ekran görüntüsünü ekledim. Kendi sitemiz için benzer bir yapıyı kurmanın maliyeti nedir?",
            "modality": "multimodal_image",
            "intent": "solve",
            "persona": "technical_buyer",
            "cluster_label": "competitor_ui_tr",
            "image_context": f"Rakip firmanın {topic} hizmetlerine ait fiyat ve özellik tablosu ekran görüntüsü",
        },
    ]
    if brand:
        prompts.append({
            "prompt": f"{brand} firmasının {topic} hizmetleri güvenilir mi? Çalışan veya hizmet alan müşterilerin gerçek deneyimleri ve şikayetleri nelerdir?",
            "modality": "text",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "brand_trust_tr",
        })
    return prompts

def _generate_arabic_prompts(topic: str, site: WebsiteContext | None) -> list[dict[str, Any]]:
    brand = site.brand if site and site.brand else ""
    prompts = [
        {
            "prompt": f"ما هي أفضل الشركات الموثوقة لتقديم خدمات {topic}؟ وما هي معايير المفاضلة بينها وبين المنافسين؟",
            "modality": "text",
            "intent": "learn",
            "persona": "business_owner",
            "cluster_label": "top_providers_ar",
        },
        {
            "prompt": f"كم تبلغ التكلفة المتوسطة لخدمات {topic} شهرياً؟ وكيف أتحقق من أن عرض السعر المقدم عادل وليس مبالغاً فيه؟",
            "modality": "text",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "pricing_ar",
        },
        {
            "prompt": f"مرحباً شات جي بي تي، أحتاج نصيحة سريعة حول الاستثمار في {topic}. هل من الأفضل توظيف فريق داخلي أم التعاقد مع وكالة متخصصة؟",
            "modality": "voice",
            "intent": "compare",
            "persona": "business_owner",
            "cluster_label": "voice_ar",
            "voice_markers": "مرحباً شات جي بي تي...",
        },
        {
            "prompt": f"أرفقت لقطة شاشة لعرض الأسعار وتفاصيل خدمات {topic}. هل هذه البنود والأسعار منطقية وفقاً لمعايير السوق الحالية؟",
            "modality": "multimodal_image",
            "intent": "buy",
            "persona": "budget_conscious_buyer",
            "cluster_label": "quote_audit_ar",
            "image_context": f"لقطة شاشة لعرض سعر رسمي يوضح تفاصيل وساعات العمل لخدمات {topic}",
        },
    ]
    if brand:
        prompts.append({
            "prompt": f"ما هو تقييم شركة {brand} في مجال {topic}؟ وهل تجارب العملاء معهم إيجابية وملتزمة بالمواعيد؟",
            "modality": "text",
            "intent": "trust",
            "persona": "skeptical_customer",
            "cluster_label": "brand_trust_ar",
        })
    return prompts

def generate_realistic_prompts(
    topic: str,
    site: WebsiteContext | None = None,
    lang: str = "auto",
    modalities: list[str] | None = None,
    count: int = 30
) -> list[Question]:
    """Generates authentic, diverse questions matching real human AI search queries.
    Stratifies across text, voice dictation, and multimodal vision prompts.
    """
    if lang == "auto":
        from .extractor import detect_language
        lang = detect_language(f"{topic} {site.title if site else ''}")

    allowed_modalities = set(modalities) if modalities else {"text", "voice", "multimodal_image"}
    if "all" in allowed_modalities:
        allowed_modalities = {"text", "voice", "multimodal_image"}

    raw_items: list[dict[str, Any]] = []
    if lang == "fa":
        raw_items = _generate_persian_prompts(topic, site)
    elif lang == "tr":
        raw_items = _generate_turkish_prompts(topic, site)
    elif lang == "ar":
        raw_items = _generate_arabic_prompts(topic, site)
    else:
        raw_items = _generate_english_prompts(topic, site)

    # Filter by modality if requested
    filtered = [item for item in raw_items if item["modality"] in allowed_modalities]
    if not filtered:
        filtered = raw_items

    questions: list[Question] = []
    for idx, item in enumerate(filtered, start=1):
        prompt_text = item["prompt"]
        intent = item.get("intent") or classify_intent(prompt_text)
        stage_name = classify_stage(intent)
        modality = item.get("modality", "text")
        
        source_ref = f"answerpath:{modality}"
        pid = f"AP-PRM-{idx:03d}"

        q = Question(
            id=pid,
            text=prompt_text,
            prompt=prompt_text,
            source=source_ref,
            evidence="generated",
            intent=intent,
            stage=stage_name,
            frequency=1,
            cluster=idx,
            modality=modality,
            persona=item.get("persona", "general_user"),
            source_type="generated",
            source_reference=source_ref,
            cluster_label=item.get("cluster_label", "general_query"),
            image_context=item.get("image_context", ""),
            voice_markers=item.get("voice_markers", ""),
            language=lang,
            target_entities=[site.brand] if site and site.brand else []
        )
        questions.append(q)
        if len(questions) >= count:
            break

    return questions
