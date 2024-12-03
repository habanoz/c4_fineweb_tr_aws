
from trfineplus_filter import *
from dummy_disk_writer import DummyDiskWriter
from datatrove.data import Document

def test_filter_max_word_length_no_pass():
    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass,reason = filter.filter(Document(text="aliatabakaaliatabakaaliatabaka", id=0))
    assert not is_pass
    assert reason == "max_word_length"
    
def test_filter_max_word_length_pass():
    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass = filter.filter(Document(text="aliatabaka", id=0))
    assert is_pass == True
    
def test_filter_max_diamond_char_perc_no_pass():
    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass,reason = filter.filter(Document(text="���123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 ", id=0))
    assert not is_pass
    assert reason == "max_diamond_char_perc"
    
def test_filter_max_diamond_char_perc_pass():
    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass = filter.filter(Document(text="�123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 ", id=0))
    assert is_pass == True

def test_filter_black_list_words():
    text = """Adana Uluslararası Portakal Çiçeği Karnavalı'nde Kostümlü Halk Koşusu - Rotka Adana Uluslararası Portakal Çiçeği Karnavalı'nde Kostümlü Halk Koşusu - Rotka
Ana sayfa YAŞAM Adana Uluslararası Portakal Çiçeği Karnavalı’nde Kostümlü Halk Koşusu
Adana Uluslararası Portakal Çiçeği Karnavalı’nde Kostümlü Escort Eskişehir Halk Koşusu"""

    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass,reason = filter.filter(Document(text, id=0))
    assert not is_pass
    assert reason == "black_list_words"
    
def test_filter_non_recovarable():
    text = """Hamilelik dï¿½neminde rahatï¿½a kullanï¿½lacak tarzda hazï¿½rlanmï¿½ï¿½ kï¿½sa kollu t-shirt.
Standart, her bedende bulunur.
Bebeï¿½in bulunduï¿½u karï¿½n bï¿½lgesinde kullanï¿½lan ï¿½zel kumaï¿½ sayesinde %100 elektromanyetik radyasyondan korur."""

    logs = []
    test_writer=DummyDiskWriter(logs)
    filter = TrFinePlusFilter(test_writer)
    is_pass,reason = filter.filter(Document(text, id=0))
    assert not is_pass
    assert reason == "non_recoverable_chars"
    