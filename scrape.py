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
    name = None
    name = soup.find(class_='node-title')
    if name:
        data_dict['Name'] = name.get_text(strip=True)
    else:
       pass

    # Simple adress
    simple_adress = None
    simple_adress = soup.find(class_='adress-simple')
    if simple_adress:
        data_dict['Simple Adress'] = simple_adress.get_text(strip=True)
    else:
       pass

    # Cellphone number
    cellphone_number = None
    cellphone_number = soup.find(class_= 'field--type-telephone')
    if cellphone_number:
        data_dict['Cellphone Number'] = cellphone_number.get_text(strip=True)
    else:
       pass

    # Email
    span_element = None
    span_element = soup.find('span', class_='__cf_email__')
    if span_element:
        match = re.search(r'data-cfemail="(.+?)"', str(span_element))
        data_dict['Company Email'] = cfDecodeEmail(match.group(1)) if match else None

    # Website
    website = None
    website = soup.find(class_= 'field-name-field-website-url')
    if website:
        data_dict['Site'] = website.get_text(strip=True)
    else:
       pass

    # Youtube
    youtube_link = None  
    youtube_tag = soup.find(class_='field--name-field-company-youtube')

    if youtube_tag:
        youtube_link = youtube_tag.find('a')['href']
        data_dict['Youtube Link'] = youtube_link
    else:
        data_dict['Youtube Link'] = youtube_link

    # Territory covered
    territory = None
    territory = soup.find(class_='field--type-country-area')
    if territory:
        data_dict['Territory Covered'] = territory.get_text(strip=True)
    else:
       pass

    # Lines of business
    lines_business = None
    lines_business = soup.find(class_='field--name-field-business-lines')
    if lines_business:
        data_dict['Lines of Business'] = lines_business.get_text(strip=True)
    else:
       pass

    # Manufacturers represented
    manufacturers_represented = None
    manufacturers_represented = soup.find(class_='field--name-field-manufacturers-represented')
    if manufacturers_represented:
        data_dict['Manufacturers Represented'] = manufacturers_represented.get_text(strip=True)
    else:
       pass

    #Fax
    fax_div = None
    fax_div = soup.find('div', class_='field-name-field-fax-number')

    if fax_div:
        fax_number_with_label = ' '.join(fax_div.stripped_strings)
        label = 'Fax:'
        fax_number = fax_number_with_label[len(label):].strip()
        data_dict['Fax'] = fax_number
    else:
        pass

    #Adress
    try:
        company_section = soup.find('div', class_='company')

        if company_section:
            address1 = None
            address1 = company_section.find('span', class_='address-line1')
            if address1:
                data_dict['Address Line 1'] = address1.get_text(strip=True)
            else:
                pass
            
            address2 = None
            address2 = company_section.find('span', class_='address-line2')
            if address2:
                data_dict['Address Line 2'] = address2.get_text(strip=True)
            else:
                pass

            locality = None
            locality = company_section.find('span', class_='locality')
            if locality:
                data_dict['Locality'] = locality.get_text(strip=True)
            else:
                pass

            administrative_area = None
            administrative_area = company_section.find('span', class_='administrative-area')
            if administrative_area:
                data_dict['Administrative Area'] = administrative_area.get_text(strip=True)
            else:
                pass

            postal_code = None
            postal_code = company_section.find('span', class_='postal-code')
            if postal_code:
                data_dict['Postal Code'] = postal_code.get_text(strip=True)
            else:
                pass

            country = None
            country = company_section.find('span', class_='country')
            if country:
                data_dict['Country'] = country.get_text(strip=True)
            else:
                pass
        else:
            pass
    except AttributeError:
        pass

    try:
        contacts_section = soup.find('div', class_='primary-contacts')

        if contacts_section:
            fst_name = None
            scnd_name = None
            title = None
            fst_name = contacts_section.find(
                'div', class_='field--name-field-primary-contact-first-name')
            scnd_name = contacts_section.find(
                'div', class_='field--name-field-primary-contact-last-name')

            if fst_name and scnd_name:
                full_name = f"{fst_name.get_text(strip=True)} {scnd_name.get_text(strip=True)}"

                title = contacts_section.find(
                    'div', class_='field--name-field-primary-contact-title')
                if title:
                    full_name += f", {title.get_text(strip=True)}"

                data_dict['Contact name'] = full_name
            else:
                pass
        else:
            pass

        mobile = None
        mobile = contacts_section.find('div', class_='field-name-field-primary-contact-mobile')
        if mobile:
            mobile_with_label = ' '.join(mobile.stripped_strings)
            label = 'Mobile:'
            mobile_number = mobile_with_label[len(label):].strip()
            data_dict['Primary Number Contact'] = mobile_number
        else:
            pass
        
        email_span = None
        email_span = soup.find('div', class_='field--name-field-primary-contact-email')
        match = re.search(r'data-cfemail="(.+?)"', str(email_span))

        if email_span:
            if match:
                encrypted_email = match.group(1)
                decoded_email = cfDecodeEmail(encrypted_email)

                data_dict['Primary Email Contact'] = decoded_email
            else:
                pass
            
    except AttributeError:
        pass

    #Description
    
    description = None
    description = soup.find('div', class_='field--name-field-company-description')
    if description:
        data_dict['Description'] = description.get_text(strip=True)
    else:
        pass

    # Industries served 
    industries_served = soup.find('div', class_='field--name-field-industries-served-other')
    if industries_served:
        data_dict['Industries Served'] = industries_served.get_text(strip=True)
    else:
        pass

    #Equipment Sold
    type_equipment = None
    type_equipment = soup.find('div', class_='field--name-field-equipment-sold-type-other')
    if type_equipment:
        data_dict['Type of Equipment'] = type_equipment.get_text(strip=True)

    #Provide sales after service?
    sales_after_service = None
    sales_after_service = soup.find('div', class_='field--name-field-after-sales-service')
    if sales_after_service:
        data_dict['Sales After Service'] = sales_after_service.get_text(strip=True)
    else:
        pass

    data_list.append(data_dict)

for link in links:
    scrape_page(link)
