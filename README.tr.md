# AnswerPath GEO — Türkçe

[![PyPI version](https://img.shields.io/pypi/v/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![Python versions](https://img.shields.io/pypi/pyversions/answerpath-geo.svg)](https://pypi.org/project/answerpath-geo/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AnswerPath GEO, SEO, GEO (Generative Engine Optimization) ve AEO için kullanıcıların yapay zekâya (ChatGPT, Perplexity, Claude, Gemini) yönelttiği gerçekçi konuşma, sesli dikte ve çok modlu (ekran görüntüsü / görsel) soruları keşfeder ve modeller.

## Hızlı kullanım

```bash
pip install answerpath-geo
answerpath "e-ticaret SEO danışmanlığı"
```

Web sitesi URL'si ile doğrudan analiz:

```bash
answerpath https://example.com --modality all --count 30
```

`observed` sizin verinizde gerçekten görülen sorudur; `generated` araştırma hipotezidir. Çıktılar `answerpath-output/` dizininde JSON, CSV ve GEO-Scope uyumlu benchmark formatında kaydedilir.

Araç yerel çalışır; API anahtarı, LLM, GPU veya harici hesap girişi gerekmez.

[PyPI](https://pypi.org/project/answerpath-geo/) · [GitHub](https://github.com/tmolavi/answerpath-geo) · [Molavi.pro](https://molavi.pro)
