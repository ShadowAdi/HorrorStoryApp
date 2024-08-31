from bs4 import BeautifulSoup
import requests

# Function to parse HTML content and extract story links
def get_story_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")  # Use response.text to get HTML content
    story_links = []

    for link in soup.find_all("a", class_="read_button"):  # Adjust the class name as needed
        story_links.append(link.get("href"))  # Get the href attribute of the <a> tag

    return soup, story_links

# Function to find the URL of the next page
def get_next_page_url(soup):
    next_div = soup.find("div", class_="next-posts")
    if next_div:
        next_page = next_div.find("a")
        if next_page:
            return next_page.get("href")

    return None

# Function to scrape all stories and save them to a file
def get_all_story(start_url, output_file):
    current_url = start_url
    all_story_links = []

    while current_url:
        print(f"Scraping Page: {current_url}")

        soup, story_links = get_story_link(current_url)
        all_story_links.extend(story_links)

        current_url = get_next_page_url(soup)

    with open(output_file, "w") as file:
        for story in all_story_links:
            file.write(story + "\n")

    print(f"All story links have been saved to {output_file}")

# Start URL of the website's first page
start_url = "https://www.thedarkmagazine.com/fiction/"

# Output file to save story links
output_file = 'story_links.txt'

# Start scraping and save story links
get_all_story(start_url, output_file)
