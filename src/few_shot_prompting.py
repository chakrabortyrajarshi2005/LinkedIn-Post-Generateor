import json
import pandas as pd
class FewShotPrompting:
    def __init__(self, file_path="data/processed-post.json"):
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)
    
    def load_posts(self,file_path):
        with open (file_path, encoding="utf-8") as file:
            posts = json.loads(file)
            df = pd.json.normalize(posts)
            

if __name__ == "__main__":
    file_system = FewShotPrompting()
    pass