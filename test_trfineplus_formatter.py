from dummy_disk_writer import DummyDiskWriter
from datatrove.data import Document
from trfineplus_formatter import TrFinePlusFormatter

def test_fix_windows_1252_chars():
    text = "Birleşmiş Milletler\x92in (BM) Kıbrıs sorunuyla ilgili üçlü görüşme hazırlığının devam ettiği bildirildi.\nFileleftheros gazetesi \x93Kasım Belirleyici Ay\x94 başlıklı"
    text_fix = "Birleşmiş Milletler'in (BM) Kıbrıs sorunuyla ilgili üçlü görüşme hazırlığının devam ettiği bildirildi.\nFileleftheros gazetesi \"Kasım Belirleyici Ay\" başlıklı"
    
    formatter=TrFinePlusFormatter()
    assert formatter.format(text) == text_fix

def test_broken_tr_chars():
    text = """KURTULUÞ CEPHESÝ. Bilimadamý nýn Medya Serüveni. Kan Tadý. Yeni-Osmanlýcý Efendi Bir Bilimadamý. Sabetaycýlýk
Download "KURTULUÞ CEPHESÝ. Bilimadamý nýn Medya Serüveni. Kan Tadý. Yeni-Osmanlýcý Efendi Bir Bilimadamý. Sabetaycýlýk"""
    
    correct_text="""KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık
Download "KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık"""

    formatter=TrFinePlusFormatter()
    assert formatter.format(text) == correct_text
    
def test_double_lines():
    text="""KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık - PDF
KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık
Download "KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık"""

    dedup_text="""KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık
Download "KURTULUŞ CEPHESİ. Bilimadamı nın Medya Serüveni. Kan Tadı. Yeni-Osmanlıcı Efendi Bir Bilimadamı. Sabetaycılık"""

    formatter=TrFinePlusFormatter()
    assert formatter.format(text) == dedup_text

