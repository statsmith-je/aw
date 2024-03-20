import pandas as pd
from pptx import Presentation

class Pres():
    def __init__(self, modules, files):
        self._files = files
        self._modules = modules

    @property
    def file_list(self):
        return self._files
    
    @property
    def module_list(self):
        return self._modules
    
    def extract_info(self): 
        data = pd.DataFrame(columns = ["Module", "Slide", "Title", "Notes"])
        for num, file in enumerate(self._files):   
            prs = Presentation(file)
            for slide_num, slide in enumerate(prs.slides):
                slide_num +=1
                try:
                    title = slide.shapes.title.text
                except:
                    title = pd.NA
                data.loc[len(data)] = [self._modules[num], slide_num, title]
            self.info = data

    
