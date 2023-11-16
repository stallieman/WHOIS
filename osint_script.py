# osint_script.py
import requests
from bs4 import BeautifulSoup

def get_domain_info(domain):
    url = f'https://www.whois.com/whois/{domain}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    domain_info = {
        'Domain': domain,
        'Registrar': get_info(soup, 'Registrar'),
        'Creation Date': get_info(soup, 'Creation Date'),
        'Expiration Date': get_info(soup, 'Expiration Date'),
    }

    return domain_info

def get_info(soup, label):
    try:
        return soup.find('div', {'class': 'df-block whois-info'}).find('div', {'class': 'df-value'}, string=label).find_next('div', {'class': 'df-value'}).text.strip()
    except AttributeError:
        return f"Not found: {label}"

if __name__ == "__main__":
    domain_name = input("Enter the domain name: ")
    domain_info = get_domain_info(domain_name)

    if domain_info:
        print("\nDomain Information:")
        for key, value in domain_info.items():
            print(f"{key}: {value}")
