"""Public provenance and privacy-boundary regression tests for entity discovery."""
import copy
import json
from pathlib import Path
from urllib.parse import urlparse
import pytest
from scripts.build_robotics_site import _validate_public_entities, build

ROOT = Path(__file__).resolve().parents[1]

def payload():
    return json.loads((ROOT / 'intelligence/entities.json').read_text(encoding='utf-8'))

def test_public_entity_schema_and_references():
    data = payload()
    _validate_public_entities(data)
    nodes = {n['id'] for n in json.loads((ROOT/'intelligence/mindmap.json').read_text(encoding='utf-8'))['nodes']}
    orgs = {o['id'] for o in data['organizations']}
    people = {p['id'] for p in data['people']}
    assert len(orgs) == len(data['organizations'])
    assert len(people) == len(data['people'])
    for org in data['organizations']:
        assert org.get('map_node_id', next(iter(nodes))) in nodes
    for person in data['people']:
        if person.get('organization_id'):
            assert person['organization_id'] in orgs
        if person.get('linkedin_url'):
            assert urlparse(person['linkedin_url']).hostname in ('linkedin.com', 'www.linkedin.com')
    for a in data['associations']:
        assert a['node_id'] in nodes and a['organization_id'] in orgs
        if a.get('via_node_id'):
            assert a['via_node_id'] in nodes
    for c in data['contributions']:
        assert c['node_id'] in nodes and c['person_id'] in people
    for collection in ['people', 'associations', 'contributions']:
        for item in data[collection]:
            assert item['sources'] and item['verified_on']
            assert all(s['url'].startswith('https://') for s in item['sources'])

@pytest.mark.parametrize('private_key', ['notes', 'priority', 'outreach_draft', 'contacted', 'readiness', 'next_follow_up'])
def test_private_fields_cannot_be_exported(private_key):
    data = copy.deepcopy(payload())
    data['people'][0][private_key] = 'PRIVATE_SENTINEL'
    with pytest.raises(ValueError, match='Non-public'):
        _validate_public_entities(data)

def test_source_fields_cannot_smuggle_private_state():
    data = copy.deepcopy(payload())
    data['people'][0]['sources'][0]['notes'] = 'PRIVATE_SENTINEL'
    with pytest.raises(ValueError, match='sources'):
        _validate_public_entities(data)

def test_build_exports_exact_public_payload():
    build()
    assert json.loads((ROOT/'site/data/entities.json').read_text(encoding='utf-8')) == payload()
    assert not list((ROOT/'site').rglob('private-records.json'))
