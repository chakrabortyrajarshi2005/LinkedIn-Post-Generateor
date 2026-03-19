import json

def extract_metadata(post):    
    post
    return {
        "line-count": 15,
        "language": "english",
        "tags": ["AI", "Machine Learning", "Business Use cases of AI"],
    }


def processed_posts(raw_post_path, processed_post_path="data/processed-post.json"):
    good_post = []
    with open(raw_post_path, encoding="utf-8") as file:
        posts = json.load(file)
        # print(posts)
        # print(type(posts))
        
        for post in posts :
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata
            
            good_post.append(post_with_metadata)
            
    for x in good_post: 
        print(x)


if __name__ == "__main__":
    processed_posts("data/raw-post.json", "data/processed-post.json")

