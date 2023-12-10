
import requests
from bs4 import BeautifulSoup


def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    blog_links = []

    for article in soup.find_all('article'):
        for link in article.find_all('a'):
            link_url = link.get('href')
            if link_url and link_url.startswith('https://aws.amazon.com/blogs/') and ("/category/" not in link_url):
                #print(link_url)
                blog_links.append(link_url)
                break
        for datepublished in article.find_all('time'):
            isodt = datepublished.get('datetime')

    return blog_links



starting_page = "https://aws.amazon.com/es/blogs/machine-learning/"


blogs = get_all_links(starting_page)
for i in range (1,150):
    url = f"{starting_page}/page/{i}/"
    blogs += get_all_links(url)

print (f"se encontraron {len(blogs)} blogs")


rows_per_file = 100

# Split the data into chunks of 100 rows each
chunks = [blogs[i:i + rows_per_file] for i in range(0, len(blogs), rows_per_file)]


for index, chunk in enumerate(chunks, start=1):
    output_file = f'ml_blogs_{index}.txt'
    # Save the data to the file
    with open(output_file, 'w') as file:
        for item in chunk:
            file.write(f"{item}\n")
    print(f"Data saved to {output_file}")