import json

def processed_posts(raw_post_path, processed_post_path="data/processed-post.json"):
    with open(raw_post_path, encoding="utf-8") as file:
        posts = json.load(file)
        print(posts)
        print(type(posts))


if __name__ == "__main__":
    processed_posts("data/raw-post.json", "data/processed-post.json")
