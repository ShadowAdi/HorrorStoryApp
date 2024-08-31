from bs4 import BeautifulSoup
import requests
import json

file1 = open("story_links.txt", "r")
Lines = file1.readlines()



def Story_Scrapper(url):
    story_info = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    storyTitleDiv = soup.find("h2", class_="entry-title")
    if storyTitleDiv:
        storyTitle = storyTitleDiv.find("span")
        story_info["title"] = storyTitle.text.strip()

    storyWrittenBy = soup.find("h4", class_="byline")
    if storyWrittenBy:
        storyWrittenByA = storyWrittenBy.find("a")
        if storyWrittenByA:
            story_info["Author"] = storyWrittenByA.get_text().strip()
            story_info["AuthorLink"] = storyWrittenByA.get("href")

    contentDiv = soup.find("div", class_="entry-content")
    if contentDiv:
        paragraphs = contentDiv.find_all("p")
        story_info["content"] = "\n".join(
            p.get_text().strip() for p in paragraphs[:-1]
        ) 

    return story_info



def Story_File():
    all_stories=[]
    count=0
    
    for line in Lines:
        count += 1
        story_info=Story_Scrapper(line.strip())
        all_stories.append(story_info)
        print("Line{}: {}".format(count, line.strip()))

    with open("Story.json","w") as json_file:
        json.dump(all_stories,json_file,indent=4)
    

    print("All stories have been saved to Story.json")

Story_File()



