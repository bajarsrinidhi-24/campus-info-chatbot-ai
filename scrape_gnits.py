import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin

def scrape_gnits_website(base_url="https://gnits.ac.in"):
    """Scrape all text content from GNITS website"""
    
    visited = set()
    all_data = []
    
    def scrape_page(url):
        if url in visited:
            return
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return
            visited.add(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script, style tags
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Store
            all_data.append({
                "source": url,
                "content": text[:5000]  # Limit per page
            })
            
            # Find and scrape subpages
            for a in soup.find_all('a', href=True):
                href = a['href']
                full_url = urljoin(url, href)
                if 'gnits.ac.in' in full_url and full_url not in visited:
                    scrape_page(full_url)
                    
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    # Start scraping
    scrape_page(base_url)
    
    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/gnits_website_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"✅ Scraped {len(all_data)} pages")
    return all_data

def create_handbook_data():
    """Create handbook data"""
    handbook_content = """
    GNITS STUDENT HANDBOOK 2025
    
    ACADEMIC RULES:
    - Minimum attendance required: 75%
    - Exam structure: Mid exams (30 marks) + End semester (70 marks)
    - Grading: O (≥90%), A+ (85-89%), A (80-84%), B+ (75-79%)
    
    FACILITIES:
    - Library timings: 8 AM to 8 PM (Monday-Saturday)
    - Hostel: Separate hostels for girls with 24/7 security
    - Canteen: Vegetarian and non-vegetarian options
    
    CLUBS:
    - Coding Club, Robotics Club, Entrepreneurship Cell
    - Cultural Committee, Technical Club (ACM)
    
    CONTACTS:
    - Principal: 040-29565850
    - Admissions: 040-29565856
    - Placements: 040-29565860
    """
    
    os.makedirs("data", exist_ok=True)
    with open("data/gnits_handbook.txt", "w", encoding="utf-8") as f:
        f.write(handbook_content)
    
    print("✅ Created handbook data")

if __name__ == "__main__":
    print("Starting GNITS data collection...")
    scrape_gnits_website()
    create_handbook_data()
    print("✅ All data collected!")
