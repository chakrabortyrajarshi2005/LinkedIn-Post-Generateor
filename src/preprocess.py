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
    res = chain.invoke({"post": post})

    try:
        json_parser = JsonOutputParser()
        response = json_parser.parse(res.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return response


def get_unified_tags(post_with_metadata):
    unique_tags = set()
    for post in post_with_metadata:
        unique_tags.update(post["tags"])

    unique_tags_list = ",".join(unique_tags)

    prompt_template = """I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list. 
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    3. Output should have mapping of original tag and the unified tag. 
       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
    
    Here is the list of tags: 
    {tags}
    """

    promptTemplate = PromptTemplate.from_template(prompt_template)
    chain = promptTemplate | llm
    res = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        response = json_parser.parse(res.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")
    return response


def processed_posts(raw_post_path, processed_post_path="../data/processed-post.json"):
    good_post = []
    with open(raw_post_path, encoding="utf-8") as file:
        posts = json.load(file)
        # print(posts)
        # print(type(posts))

        for post in posts:
            metadata = extract_metadata(post["text"])
            post_with_metadata = post | metadata

            good_post.append(post_with_metadata)
        
    unified_tags_mapping = get_unified_tags(good_post)
    
    for post in good_post:
        current_tags = post['tags']
        new_tags = {unified_tags_mapping[tag] for tag in current_tags}
        post['tags'] = list(new_tags)
        
    with open(processed_post_path, encoding='utf-8', mode="w") as outfile:
        json.dump(good_post, outfile, indent=4)


if __name__ == "__main__":
    processed_posts("../data/raw-post.json", "../data/processed-post.json")
