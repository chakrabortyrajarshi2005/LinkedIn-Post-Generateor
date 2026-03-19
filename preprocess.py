import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_integration import llm

def extract_metadata(post):
    prompt_template = """
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble. 
    2. JSON object should have exactly three keys: line_count, language and tags. 
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)
    
    Here is the actual post on which you need to perform this task:  
    {post}
    """
    
    promptTemplate = PromptTemplate.from_template(prompt_template)
    chain = promptTemplate | llm
    res=chain.invoke({"post":post})
    
    try:
        json_parser = JsonOutputParser()
        response = json_parser.parse(res.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return response


def processed_posts(raw_post_path, processed_post_path="data/processed-post.json"):
    good_post = []
    with open(raw_post_path, encoding="utf-8") as file:
        posts = json.load(file)
        # print(posts)
        # print(type(posts))

        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata

            good_post.append(post_with_metadata)

    for x in good_post:
        print(x)


if __name__ == "__main__":
    processed_posts("data/raw-post.json", "data/processed-post.json")
