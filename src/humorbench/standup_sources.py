import requests
from bs4 import BeautifulSoup, SoupStrainer

def scrape_standup_sources():
    response = requests.get("https://scrapsfromtheloft.com/stand-up-comedy-scripts/")

    found = set()

    for link in BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            link_text = link['href']
            link_text_split = link_text.split('/')
            if "comedy" in link_text and link_text not in found and "comedy" != link_text_split[-2]:
                transcript_name = link_text_split[-2]
                found.add(link_text)
                with open(f"transcripts/{transcript_name}.txt", 'a+') as f:
                    transcript_response = requests.get(link_text)
                    for tag in BeautifulSoup(transcript_response.text, 'html.parser', parse_only=SoupStrainer('p')):
                        if tag.has_attr('style') and "text-align: justify;" in tag.attrs['style']:
                            f.write(tag.text + '\n')

def insert_linebreaks(file_path):
    new_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if "]" in line:
                split_lines = ["[" + e for e in line.split("[")]
            else:
                split_lines = [line]
            new_lines += split_lines
        new_lines = "\n".join(new_lines)
    with open(file_path, 'w') as file:
        file.write(new_lines)
if __name__ == "__main__":
    insert_linebreaks("/home/wisp/cmsc723fall25/humorbench/datasets/transcripts/al-madrigal-why-is-the-rabbit-crying-2013-full-transcript.txt")