import nltk, codecs


class God:
    def __init__(self, fname):
        self.fname = fname
        pass
    def load(self):
        return codecs.open(self.fname, "rb", encoding="utf-8").read()
    def run(self):
        text = self.load()
        # tokenize
        tokens = nltk.word_tokenize(text)
        
        print tokens[:100]
        

class HtmlParser:
    def __init__(self, fname):
        self.fname = fname
    def run(self):
        text = codecs.open(self.fname, "rb", encoding="utf-8").read()
        
    

if __name__ == "__main__":
    fname = "/home/loj/Downloads/Far_From_The_Madding_Crowd-Thomas_Hardy.txt"
    g = God(fname)
    g.run()
    
    h = HtmlParser("/home/loj/Downloads/list.html")
    h.run()
    
    print "end"
