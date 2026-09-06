import json
from answerpath_geo.core import extract_records, mine, write_outputs

def test_observed_and_generated_are_labeled(tmp_path):
    p=tmp_path/'chat.json'; p.write_text(json.dumps({'messages':[{'role':'user','content':'What is the best accounting service?'}]}))
    qs=mine('accounting service', extract_records(p))
    assert any(q.evidence=='observed' for q in qs)
    assert all(q.evidence in {'observed','generated','observed+generated'} for q in qs)

def test_no_generated(tmp_path):
    qs=mine('seo', [('How much does SEO cost?', 'x')], include_generated=False)
    assert len(qs)==1 and qs[0].evidence=='observed' and qs[0].intent=='buy'

def test_outputs(tmp_path):
    out=write_outputs(mine('web design', [], True), tmp_path/'out')
    assert (out/'questions.json').exists() and (out/'questions.csv').exists()

def test_mcp_protocol():
    from answerpath_geo.mcp import handle
    assert handle({'jsonrpc':'2.0','id':1,'method':'initialize','params':{}})['result']['serverInfo']['name']=='answerpath-geo'
    out=handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'discover_questions','arguments':{'topic':'web design','include_generated':False,'inputs':[{'text':'How much does web design cost?','source':'test'}]}}})
    assert out['result']['structuredContent']['questions'][0]['intent']=='buy'
