import json
from unittest.mock import patch
from answerpath_geo.core import extract_records, mine, write_outputs, classify, stage
from answerpath_geo.extractor import extract_website_context, is_url, detect_language

def test_observed_and_generated_are_labeled(tmp_path):
    p = tmp_path / 'chat.json'
    p.write_text(json.dumps({'messages': [{'role': 'user', 'content': 'What is the best accounting service?'}]}))
    qs = mine('accounting service', extract_records(p))
    assert any(q.evidence == 'observed' for q in qs)
    assert all(q.evidence in {'observed', 'generated', 'observed+generated'} for q in qs)

def test_no_generated(tmp_path):
    qs = mine('seo', [('How much does SEO cost?', 'x')], include_generated=False)
    assert len(qs) == 1 and qs[0].evidence == 'observed' and qs[0].intent == 'buy'

def test_outputs(tmp_path):
    out = write_outputs(mine('web design', [], True), tmp_path / 'out')
    assert (out / 'questions.json').exists() and (out / 'questions.csv').exists()
    assert (out / 'benchmark_prompts.json').exists()

def test_mcp_protocol():
    from answerpath_geo.mcp import handle
    init_res = handle({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {}})
    assert init_res['result']['serverInfo']['name'] == 'answerpath-geo'
    out = handle({
        'jsonrpc': '2.0',
        'id': 2,
        'method': 'tools/call',
        'params': {
            'name': 'discover_questions',
            'arguments': {
                'topic': 'web design',
                'include_generated': False,
                'inputs': [{'text': 'How much does web design cost?', 'source': 'test'}]
            }
        }
    })
    assert out['result']['structuredContent']['questions'][0]['intent'] == 'buy'

def test_persian_natural_conversational_queries():
    topic = "طراحی سایت فروشگاهی"
    qs = mine(topic, include_generated=True, lang="fa")
    assert len(qs) > 5
    # Must not contain robotic English fragments like "What is the best طراحی سایت..."
    for q in qs:
        assert "What is the best" not in q.text
        assert "small business" not in q.text

    # Verify voice dictation queries exist
    voice_qs = [q for q in qs if q.modality == "voice"]
    assert len(voice_qs) > 0
    assert any("چت‌جی‌پی‌تی" in q.text or "سلام" in q.text for q in voice_qs)

    # Verify multimodal vision queries exist
    vision_qs = [q for q in qs if q.modality == "multimodal_image"]
    assert len(vision_qs) > 0
    assert any(q.image_context for q in vision_qs)

def test_multimodal_and_voice_modalities_filter():
    topic = "Cloud Hosting"
    # Only voice
    voice_only = mine(topic, modalities="voice", lang="en")
    assert all(q.modality == "voice" for q in voice_only)
    assert any("ChatGPT" in q.text or "Claude" in q.text for q in voice_only)

    # Only multimodal image
    image_only = mine(topic, modalities="multimodal_image", lang="en")
    assert all(q.modality == "multimodal_image" for q in image_only)
    assert all(bool(q.image_context) for q in image_only)

def test_website_url_handling_and_mocked_extraction():
    url = "https://novin.com"
    assert is_url(url)
    assert is_url("novin.com")
    assert not is_url("خدمات سئو فروشگاهی")

    # Extraction from URL (online or offline fallback)
    ctx = extract_website_context("https://novin.com")
    assert ctx.brand.lower() in {"novin", "نوین"}
    assert "novin.com" in ctx.domain

    # Mine with URL directly
    qs = mine(url, count=10)
    assert len(qs) > 0
    # Injected brand Novin / نوین in generated queries
    assert any("نوین" in q.text or "novin" in q.text.lower() for q in qs)

def test_benchmark_format_export(tmp_path):
    bench_data = mine("سئو سایت", benchmark_format=True, count=10)
    assert isinstance(bench_data, list)
    assert len(bench_data) > 0
    item = bench_data[0]
    assert "id" in item
    assert "prompt" in item
    assert "intent" in item
    assert "modality" in item
    assert "source_type" in item
    assert "cluster" in item

    # Export to disk and verify
    out = write_outputs(bench_data, tmp_path / "bench_out", benchmark_format=True)
    bench_file = out / "benchmark_prompts.json"
    assert bench_file.exists()
    loaded = json.loads(bench_file.read_text(encoding="utf-8"))
    assert len(loaded) == len(bench_data)
    assert loaded[0]["id"] == item["id"]
