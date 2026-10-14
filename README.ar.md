# AnswerPath GEO — العربية

[![PyPI version](https://img.shields.io/pypi/v/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![Python versions](https://img.shields.io/pypi/pyversions/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

يكتشف AnswerPath GEO أسئلة المستخدمين الواقعية والمحادثات الصوتية والاستفسارات متعددة الوسائط (Multimodal) التي يطرحونها على محركات الذكاء الاصطناعي (ChatGPT, Perplexity, Claude, Gemini) لأغراض SEO و GEO و AEO.

## استخدام سريع

```bash
pip install answerpath-geo
answerpath "استشارات تحسين محركات البحث للمتاجر الإلكترونية"
```

أو عن طريق إدخال رابط الموقع مباشرة:

```bash
answerpath https://example.com --lang ar --count 30
```

تعني `observed` أن السؤال ظهر فعلاً في سجلاتك، بينما `generated` فرضية بحثية تحاكي استفسارات الذكاء الاصطناعي. تُحفظ النتائج بتنسيقات JSON و CSV ومتوافقة مع معايير بنشمارك GEO-Scope.

[PyPI](https://pypi.org/project/answerpath-geo/) · [GitHub](https://github.com/tmolavi/answerpath-geo) · [Molavi.pro](https://molavi.pro)
