# AnswerPath GEO — Azərbaycan dili

[![PyPI version](https://img.shields.io/pypi/v/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![Python versions](https://img.shields.io/pypi/pyversions/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AnswerPath GEO istifadəçilərin SEO, GEO (Generative Engine Optimization) və AEO üçün süni intellektə (ChatGPT, Perplexity, Claude, Gemini) verə biləcəyi real danışıq, səsli diktə və multimodal (ekran şəkli / şəkil) sualları kəşf edir.

## Sürətli istifadə

```bash
pip install answerpath-geo
answerpath "e-ticarət üçün SEO məsləhəti"
```

Veb-sayt URL-i ilə birbaşa analiz:

```bash
answerpath https://example.com --count 30
```

`observed` sizin məlumatınızda həqiqətən görünən sualdır; `generated` araşdırma hipotezidir. Nəticələr `answerpath-output/` qovluğunda JSON, CSV və GEO-Scope benchmark formatında saxlanılır.

Alət lokal işləyir; API açarı, LLM, GPU və ya xarici hesab girişi tələb etmir.

[PyPI](https://pypi.org/project/answerpath-geo/) · [GitHub](https://github.com/tmolavi/answerpath-geo) · [Molavi.pro](https://molavi.pro)
