import json
import os
import sys

# allow importing from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import build_reply, load_data


def test_help_response():
    data = load_data()
    r = build_reply('help', data)
    assert 'Commands' in r or 'help' in r.lower()


def test_notices_list():
    data = load_data()
    r = build_reply('notices', data)
    # With sample data we should get 'Latest notices' or at least a date line
    assert 'notices' in r.lower() or '-' in r


def test_latest_search_found():
    data = load_data()
    # sample data has 'exam' in the first notice content
    r = build_reply('latest exam', data)
    assert 'exam' in r.lower() or 'notices matching' in r.lower()
