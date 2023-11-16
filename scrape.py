from decode_email import cfDecodeEmail
from bs4 import BeautifulSoup
import requests, re

data_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def get_element_text(soup, class_name):
    element = soup.find(class_=class_name)
    return element.get_text(strip=True) if element else None


def scrape_page(url):
    data_dict = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Name
    data_dict['Name'] = get_element_text(soup, 'node-title')

    # Simple address
    data_dict['Simple Address'] = get_element_text(soup, 'adress-simple')

    # Cellphone number
    data_dict['Cellphone Number'] = get_element_text(soup, 'field--type-telephone')

    # Company email
    company_email_element = soup.find(class_='field--type-email')
    span_element = company_email_element.find('span', class_='__cf_email__')

    if span_element:
        match = re.search(r'data-cfemail="(.+?)"', str(span_element))
        data_dict['Company Email'] = cfDecodeEmail(match.group(1)) if match else None
    else:
        data_dict['Company Email'] = None

    # Website
    data_dict['Site'] = get_element_text(soup, 'field-name-field-website-url')

    # Youtube
    youtube_element = soup.find(class_='field--name-field-company-youtube')
    data_dict['Youtube Link'] = youtube_element.find('a')['href'] if youtube_element else None

    # Territory covered
    data_dict['Territory Covered'] = get_element_text(soup, 'field--type-country-area')

    # Lines of business
    data_dict['Lines of Business'] = get_element_text(soup, 'field--name-field-business-lines')

    # Manufacturers represented
    data_dict['Manufacturers Represented'] = get_element_text(soup, 'field--name-field-manufacturers-represented')

    # Fax
    fax_div = soup.find('div', class_='field-name-field-fax-number')
    data_dict['Fax'] = fax_div.find('span').get_text(strip=True) if fax_div else None

    # Address
    company_section = soup.find('div', class_='company col-md-4')
    data_dict['Address Line 1'] = get_element_text(company_section, 'address-line1')
    data_dict['Address Line 2'] = get_element_text(company_section, 'address-line2')
    data_dict['Locality'] = get_element_text(company_section, 'locality')
    data_dict['Administrative Area'] = get_element_text(company_section, 'administrative-area')
    data_dict['Postal Code'] = get_element_text(company_section, 'postal-code')
    data_dict['Country'] = get_element_text(company_section, 'country')

    # Primary contact
    contacts_section = soup.find('div', class_='primary-contacts')
    fst_name = get_element_text(contacts_section, 'field--name-field-primary-contact-first-name')
    scnd_name = get_element_text(contacts_section, 'field--name-field-primary-contact-last-name')

    if fst_name and scnd_name:
        full_name = f"{fst_name} {scnd_name}"
        title = get_element_text(contacts_section, 'field--name-field-primary-contact-title')
        if title:
            full_name += f", {title}"
        data_dict['Contact name'] = full_name

    # Mobile
    mobile = get_element_text(contacts_section, 'field-name-field-primary-contact-mobile')
    data_dict['Primary Number Contact'] = mobile.split(":")[-1].strip() if mobile else None

    # Primary Email Contact
    email_span = soup.find('div', class_='field--name-field-primary-contact-email')
    match = re.search(r'data-cfemail="(.+?)"', str(email_span))
    data_dict['Primary Email Contact'] = cfDecodeEmail(match.group(1)) if match else None

    # Description
    data_dict['Description'] = get_element_text(soup, 'field--name-field-company-description')

    # Industries served
    data_dict['Industries Served'] = get_element_text(soup, 'field--name-field-industries-served-other')

    # Type of Equipment
    data_dict['Type of Equipment'] = get_element_text(soup, 'field--name-field-equipment-sold-type-other')

    # Sales After Service
    data_dict['Sales After Service'] = get_element_text(soup, 'field--name-field-after-sales-service')

    print(data_dict)

scrape_page('https://www.pmmi.org/sales-agent-directory/profile/robertpack-bv')
