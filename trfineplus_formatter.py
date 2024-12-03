from datatrove.pipeline.formatters.base import BaseFormatter

class TrFinePlusFormatter(BaseFormatter):
    name = "🇹🇷➕ TrFinewebPlus"

    def __init__(
        self,
        first_lines_jaccard_threshold=0.5
    ):
        super().__init__()
        self.first_lines_jaccard_threshold = first_lines_jaccard_threshold
        
    def jaccard(self, doc1:list, doc2:list):
        set1 = set(doc1)
        set2 = set(doc2)
        
        intersection = len(list(set1.intersection(set2)))
        union       = len(list(set1.union(set2)))
        
        return float(intersection)/float(union)
    
    def format(self, text: str) -> str:
        lines = text.split("\n",2)
        
        if len(lines)>=3:
            line0 = lines[0]
            line1 = lines[1]
            lines_rest = lines[2]
            
            jaccard_score = self.jaccard(line0.lower().split(), line1.lower().split())
            
            if jaccard_score >= self.first_lines_jaccard_threshold:
                selected_line = min(line0, line1)
                text = f"{selected_line}\n{lines_rest}"
        
        text = text.replace('\x92',"'").replace('\x93','"').replace('\x94','"')
        text = text.replace("Þ","Ş").replace("þ","ş").replace("ý", "ı").replace("Ý","İ").replace("ð","ğ")
        
        return text