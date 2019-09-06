import pytest
from ravestate.testfixtures import *
from ravestate_nlp import prop_triples


@pytest.mark.skip(reason="TODO: Rewrite so it uses an actual context/memory interaction.")
def test_roboyqa(mocker, context_fixture, triple_fixture):
    mocker.patch.object(context_fixture, 'conf', will_return='test')
    context_fixture._properties[prop_triples] = [triple_fixture]
    import ravestate_roboyqa
    with mocker.patch('ravestate_ontology.get_session'):
        ravestate_roboyqa.roboyqa(context_fixture)
