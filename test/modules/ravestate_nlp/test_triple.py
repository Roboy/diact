import logging

import pytest

from ravestate_nlp import Triple, spacy_nlp_en, extract_triples
from testfixtures import LogCapture


def create_token(text: str):
    if not text:
        return None
    return spacy_nlp_en(text)[0]


def create_triple(subject: str = None, predicate: str = None, object: str = None):
    s = create_token(subject)
    p = create_token(predicate)
    o = create_token(object)
    return Triple(subject=s, predicate=p, object=o)


@pytest.fixture
def spacy_model():
    nlp = spacy_nlp_en
    from spacy.tokens import Doc
    if not Doc.has_extension('triples'):
        Doc.set_extension('triples', getter=extract_triples)
    return nlp


@pytest.fixture
def test_token():
    return create_token('test')


@pytest.fixture
def test_triple1():
    return create_triple('subject', 'predicate', 'test')

@pytest.fixture
def test_triple2():
    return create_triple('subject', 'predicate', 'test')

@pytest.fixture
def test_triple3():
    return create_triple('subject', 'predicate', 'test')


@pytest.fixture
def full_triple():
    return create_triple('subject', 'predicate', 'object')


def test_comparison(full_triple):
    assert full_triple == full_triple


@pytest.mark.parametrize('compared_triple',
                         [create_triple('subject', 'predicate', 'test'),
                          create_triple('subject', 'test', 'object'),
                          create_triple('test', 'predicate', 'test')]
                         )
def test_comparison_negative(full_triple, compared_triple):
    assert full_triple != compared_triple


def test_comparison_tuple(full_triple):
    assert full_triple == full_triple.to_tuple()


@pytest.mark.parametrize('compared_tuple',
                         [create_triple('subject', 'predicate', 'test').to_tuple(),
                          create_triple('subject', 'test', 'object').to_tuple(),
                          create_triple('test', 'predicate', 'test').to_tuple()]
                         )
def test_comparison_negative_tuple(full_triple, compared_tuple):
    assert full_triple != compared_tuple


def test_comparison_wrong_type(full_triple):
    assert full_triple != ''


@pytest.mark.parametrize('triple, expected_log',
                         [(create_triple('subject', 'predicate', 'object'), f'subject:predicate:object'),
                          (create_triple('subject', 'predicate', None), f'subject:predicate:'),
                          (create_triple('subject', None, 'object'), f'subject::object'),
                          (create_triple(None, 'predicate', 'object'), f':predicate:object'),
                          (create_triple('subject', None, None), f'subject::'),
                          (create_triple(None, 'predicate', None), f':predicate:'),
                          (create_triple(None, None, 'object'), f'::object')]
                         )
def test_print(triple, expected_log):
    with LogCapture() as log_capture:
        logging.info(triple)
        log_capture.check(('root', 'INFO', expected_log,))


@pytest.mark.parametrize('triple, expected_log',
                         [(create_triple('subject', 'predicate', 'object'), f'<Triple object subject:predicate:object>'),
                          (create_triple('subject', 'predicate', None), f'<Triple object subject:predicate:>'),
                          (create_triple('subject', None, 'object'), f'<Triple object subject::object>'),
                          (create_triple(None, 'predicate', 'object'), f'<Triple object :predicate:object>'),
                          (create_triple('subject', None, None), f'<Triple object subject::>'),
                          (create_triple(None, 'predicate', None), f'<Triple object :predicate:>'),
                          (create_triple(None, None, 'object'), f'<Triple object ::object>')]
                         )
def test_repr(triple, expected_log):
    with LogCapture() as log_capture:
        logging.info([triple])
        log_capture.check(('root', 'INFO', f'[{expected_log}]',))


@pytest.mark.parametrize('text_input, object',
                         [('I want vanilla ice cream', 'vanilla'),
                          ('Can i have strawberry ice cream', 'strawberry')
                          ])
def test_match_either_lemma_object_recognition(spacy_model, text_input, object):
    assert spacy_model(text_input)._.triples[0].match_either_lemma(obj={object})


@pytest.mark.parametrize('text_input, subject',
                         [("Umur's cats walks in the neighbourhood", 'Umur'),
                          ("Roboy's ice creams are delicious!", "Roboy")
                          ])
def test_match_either_lemma_subject_recognition(spacy_model, text_input, subject):
    assert spacy_model(text_input)._.triples[0].match_either_lemma(subj={subject})

@pytest.mark.parametrize('text_input, subject',
                         [("Umur's cats walks in the neighbourhood", 'Eva'),
                          ("Roboy's ice creams are delicious!", "Robot")
                          ])
def test_match_either_lemma_subject_recognition_fail(spacy_model, text_input, subject):
    assert spacy_model(text_input)._.triples[0].match_either_lemma(subj={subject}) == False

