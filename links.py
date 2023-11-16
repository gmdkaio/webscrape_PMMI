from bs4 import BeautifulSoup
import requests, re, csv

urls = ['https://www.pmmi.org/sales-agent-directory/search/results', 'https://www.pmmi.org/sales-agent-directory/search/results?page=1',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=2', 'https://www.pmmi.org/sales-agent-directory/search/results?page=3',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=4', 'https://www.pmmi.org/sales-agent-directory/search/results?page=5',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=6', 'https://www.pmmi.org/sales-agent-directory/search/results?page=7',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=8', 'https://www.pmmi.org/sales-agent-directory/search/results?page=9',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=10', 'https://www.pmmi.org/sales-agent-directory/search/results?page=11',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=12', 'https://www.pmmi.org/sales-agent-directory/search/results?page=13',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=14', 'https://www.pmmi.org/sales-agent-directory/search/results?page=15',
        'https://www.pmmi.org/sales-agent-directory/search/results?page=16', 'https://www.pmmi.org/sales-agent-directory/search/results?page=17'
        ]

tag_search = 'field-title-value'
names = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for url in urls:
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    search_divs = soup.find_all('div', class_=tag_search)

    for div in search_divs:
      names.append(div.text)
  else:
     print(f"Failed to retrieve {url}. Status code: {response.status_code}")

def format_company_name(name):
    translation_table = str.maketrans('', '', '() .,+&')
    formatted_name = name.replace(' ', '-').translate(translation_table)
    formatted_name = re.sub(r'-+', '-', formatted_name)

    formatted_url = f'https://www.pmmi.org/sales-agent-directory/profile/{formatted_name.lower()}'
    
    return formatted_url

formatted_urls = [format_company_name(name) for name in names]

# Write to CSV
with open('output.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Formatted URL'])

    for url in formatted_urls:
        csv_writer.writerow([url])

print("CSV file created: output.csv")