import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin, urlparse

def scrape_gnits_website(base_url="https://gnits.ac.in"):
    """Scrape all text content from GNITS website"""
    
    visited = set()
    all_data = []
    
    def get_links(soup, current_url):
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(current_url, href)
            # Only stay on gnits.ac.in domain
            if 'gnits.ac.in' in full_url and full_url not in visited:
                links.append(full_url)
        return links
    
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
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator='\n', strip=True)
            
            # Store
            all_data.append({
                "source": url,
                "content": text[:5000]  # Limit per page
            })
            
            # Find and scrape subpages
            for link in get_links(soup, url):
                if link not in visited:
                    scrape_page(link)
                    
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
    """Create simulated handbook data (you can replace with actual PDF text)"""
    handbook_content = """
    GNITS STUDENT HANDBOOK 2025
    
    ACADEMIC RULES:
    - Minimum attendance required: 75%
    - Exam structure: Mid exams (30 marks) + End semester (70 marks)
    - Internal assessment includes assignments, quizzes, and projects.
    - Grading: O (≥90%), A+ (85-89%), A (80-84%), B+ (75-79%), B (70-74%), C (60-69%), D (50-59%), F (<50%)
    
    CODE OF CONDUCT:
    - Students must wear ID cards inside campus.
    - Ragging is strictly prohibited and leads to immediate expulsion.
    - Mobile phones must be switched off during class hours.
    
    FACILITIES:
    - Library timings: 8 AM to 8 PM (Monday-Saturday)
    - Hostel: Separate hostels for girls with 24/7 security
    - Canteen: Vegetarian and non-vegetarian options available
    - Sports: Indoor badminton, table tennis, volleyball court, basketball court
    
    CLUBS AND COMMITTEES:
    - Coding Club (CodeChef, LeetCode competitions)
    - Robotics Club
    - Entrepreneurship Development Cell (EDC)
    - Cultural Committee (organizes Splash, annual fest)
    - Technical Club (GNITS ACM Student Chapter)
    
    CONTACTS:
    - Principal office: 040-29565850
    - Admissions: 040-29565856
    - Training & Placement Cell: 040-29565860
    - Library: 040-29565870
    
    EVENTS (Upcoming):
    - IEEE ICoECIT-2026 (AI & Quantum Computing) - March 2026
    - Splash 2026 (Annual Cultural Fest) - October 2026
    - Hackathon - February 2026
    - Alumni Meet (TU TURNO-26) - December 2026
    """
    
    os.makedirs("data", exist_ok=True)
    with open("data/gnits_handbook.txt", "w", encoding="utf-8") as f:
        f.write(handbook_content)
    
    print("✅ Created handbook data")
    return handbook_content

# Run scraping
if __name__ == "__main__":
    print("Starting GNITS data collection...")
    scrape_gnits_website()
    create_handbook_data()
    print("✅ All data collected!")
