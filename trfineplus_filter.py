from datatrove.pipeline.filters.base_filter import BaseFilter
from datatrove.pipeline.filters.gopher_repetition_filter import find_duplicates
from datatrove.pipeline.writers.disk_base import DiskWriter
from datatrove.utils.typeshelper import Languages
from datatrove.utils.word_tokenizers import load_word_tokenizer
import re

def tokenize(text):
    words = re.split(r'[\W_]+', text)
    return words

word_black_list=set(["penis", "porn", "milf", "escort", "sikiş", "sikiyor", "siken", "sikini"])

class TrFinePlusFilter(BaseFilter):
    name = "🇹🇷➕ TrFinewebPlus"

    def __init__(
        self,
        exclusion_writer: DiskWriter = None,
        max_word_length: int = 30,
        max_diamond_char_perc: int = 1,
        language: str = Languages.turkish,
    ):
        super().__init__(exclusion_writer)
        self.max_word_length = max_word_length
        self.max_diamond_char_perc = max_diamond_char_perc
        self.tokenizer = load_word_tokenizer(language)

    def filter(self, doc) -> bool | tuple[bool, str]:
        words = tokenize(doc.text.lower())
        
        if any( len(w)>=self.max_word_length for w in words):
            return False, "max_word_length"
        
        if any( w in word_black_list for w in words):
            return False, "black_list_words"
        
        if int((doc.text.count('�')/len(doc.text))*100) >= self.max_diamond_char_perc:
            return False, "max_diamond_char_perc"
        
        # 70 occurrences in 100_000 documents, does it worth it to keep this check?
        if any(c in ["ï","¿","½"] for c in doc.text):
            return False, "non_recoverable_chars"
        
        return True