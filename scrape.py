from decode_email import cfDecodeEmail
from bs4 import BeautifulSoup
from links_array import links
import requests, re

data_list = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}


def scrape_page(url):
    data_dict = {}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Name
    # Name
    name = soup.find(class_='node-title')
    data_dict['Name'] = name.get_text(strip=True) if name else None

    # Simple Address
    simple_address = soup.find(class_='adress-simple')
    data_dict['Simple Address'] = simple_address.get_text(strip=True) if simple_address else None

    # Cellphone Number
    cellphone_number = soup.find(class_='field--type-telephone')
    data_dict['Cellphone Number'] = cellphone_number.get_text(strip=True) if cellphone_number else None

    # Email
    company_email_element = soup.find(class_='field--type-email')
    span_element = company_email_element.find('span', class_='__cf_email__')
    if span_element:
        match = re.search(r'data-cfemail="(.+?)"', str(span_element))
        data_dict['Company Email'] = cfDecodeEmail(match.group(1)) if match else None
    else:
        data_dict['Company Email'] = None

    # Website
    website = soup.find(class_='field-name-field-website-url')
    data_dict['Site'] = website.get_text(strip=True) if website else None

    # YouTube
    youtube_link = None
    youtube_tag = soup.find(class_='field--name-field-company-youtube')
    data_dict['Youtube Link'] = youtube_tag.find('a')['href'] if youtube_tag else None

    # Territory Covered
    territory = soup.find(class_='field--type-country-area')
    data_dict['Territory Covered'] = territory.get_text(strip=True) if territory else None

    # Lines of Business
    lines_business = soup.find(class_='field--name-field-business-lines')
    data_dict['Lines of Business'] = lines_business.get_text(strip=True) if lines_business else None

    # Manufacturers Represented
    manufacturers_represented = soup.find(class_='field--name-field-manufacturers-represented')
    data_dict['Manufacturers Represented'] = manufacturers_represented.get_text(strip=True) if manufacturers_represented else None

    # Fax
    fax_div = soup.find('div', class_='field-name-field-fax-number')
    if fax_div:
        fax_number_with_label = ' '.join(fax_div.stripped_strings)
        label = 'Fax:'
        fax_number = fax_number_with_label[len(label):].strip()
        data_dict['Fax'] = fax_number
    else:
        data_dict['Fax'] = None

    # Address
    company_section = soup.find('div', class_='company col-md-4')
    address1 = company_section.find('span', class_='address-line1')
    data_dict['Address Line 1'] = address1.get_text(strip=True) if address1 else None

    address2 = company_section.find('span', class_='address-line2')
    data_dict['Address Line 2'] = address2.get_text(strip=True) if address2 else None

    locality = company_section.find('span', class_='locality')
    data_dict['Locality'] = locality.get_text(strip=True) if locality else None

    administrative_area = company_section.find('span', class_='administrative-area')
    data_dict['Administrative Area'] = administrative_area.get_text(strip=True) if administrative_area else None

    postal_code = company_section.find('span', class_='postal-code')
    data_dict['Postal Code'] = postal_code.get_text(strip=True) if postal_code else None

    country = company_section.find('span', class_='country')
    data_dict['Country'] = country.get_text(strip=True) if country else None

    contacts_section = soup.find('div', class_='primary-contacts')
    if contacts_section:
        fst_name = contacts_section.find('div', class_='field--name-field-primary-contact-first-name')
        scnd_name = contacts_section.find('div', class_='field--name-field-primary-contact-last-name')
        if fst_name and scnd_name:
            full_name = f"{fst_name.get_text(strip=True)} {scnd_name.get_text(strip=True)}"
            title = contacts_section.find('div', class_='field--name-field-primary-contact-title')
            if title:
                full_name += f", {title.get_text(strip=True)}"
            data_dict['Contact name'] = full_name
        else:
            data_dict['Contact name'] = None
    else:
        data_dict['Contact name'] = None

    mobile = contacts_section.find('div', class_='field-name-field-primary-contact-mobile')
    data_dict['Primary Number Contact'] = ' '.join(mobile.stripped_strings)[7:].strip() if mobile else None

    email_span = soup.find('div', class_='field--name-field-primary-contact-email')
    match = re.search(r'data-cfemail="(.+?)"', str(email_span))
    if email_span and match:
        encrypted_email = match.group(1)
        decoded_email = cfDecodeEmail(encrypted_email)
        data_dict['Primary Email Contact'] = decoded_email
    else:
        data_dict['Primary Email Contact'] = None

    # Description
    description = soup.find('div', class_='field--name-field-company-description')
    data_dict['Description'] = description.get_text(strip=True) if description else None

    # Industries Served
    industries_served = soup.find('div', class_='field--name-field-industries-served-other')
    data_dict['Industries Served'] = industries_served.get_text(strip=True) if industries_served else None

    # Type of Equipment Sold
    type_equipment = soup.find('div', class_='field--name-field-equipment-sold-type-other')
    data_dict['Type of Equipment'] = type_equipment.get_text(strip=True) if type_equipment else None

    # Sales After Service
    sales_after_service = soup.find('div', class_='field--name-field-after-sales-service')
    data_dict['Sales After Service'] = sales_after_service.get_text(strip=True) if sales_after_service else None

    data_list.append(data_dict)

for link in links:
    scrape_page(link)
