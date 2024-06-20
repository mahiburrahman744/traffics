from playwright.sync_api import sync_playwright
import random
import time

# Define user agent pools
user_agents = {
    "mobile": [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; SM-G975F Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
    ],
    "tablet": [
        'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 9; Nexus 7 Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Tablet PC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ],
    "desktop": [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
}

# Define referrer platforms
referrer_platforms = [
    'https://www.google.com',
    'https://www.facebook.com',
    'https://www.twitter.com',
    'https://www.linkedin.com',
    'https://www.instagram.com',
    'https://www.pinterest.com',
    'https://www.reddit.com',
    'https://www.bing.com',
    'https://www.yahoo.com',
    'https://www.baidu.com'
]

# Function to get a random user-agent
def get_random_user_agent():
    device_type = random.choice(list(user_agents.keys()))
    return random.choice(user_agents[device_type])

# Function to get a random referrer
def get_random_referrer():
    return random.choice(referrer_platforms)

# Function to get a random geo-location
def get_random_geolocation():
    # Expanded list of geo-locations (100 locations)
    locations = [
        {'latitude': 34.0522, 'longitude': -118.2437},  # Los Angeles, USA
        {'latitude': 40.7128, 'longitude': -74.0060},   # New York, USA
        {'latitude': 48.8566, 'longitude': 2.3522},     # Paris, France
        {'latitude': 35.6895, 'longitude': 139.6917},   # Tokyo, Japan
        {'latitude': 51.5074, 'longitude': -0.1278},    # London, UK
        {'latitude': 55.7558, 'longitude': 37.6173},    # Moscow, Russia
        {'latitude': 39.9042, 'longitude': 116.4074},   # Beijing, China
        {'latitude': -33.8688, 'longitude': 151.2093},  # Sydney, Australia
        {'latitude': -23.5505, 'longitude': -46.6333},  # São Paulo, Brazil
        {'latitude': 19.4326, 'longitude': -99.1332},   # Mexico City, Mexico
        {'latitude': 28.6139, 'longitude': 77.2090},    # New Delhi, India
        {'latitude': 55.6761, 'longitude': 12.5683},    # Copenhagen, Denmark
        {'latitude': 52.5200, 'longitude': 13.4050},    # Berlin, Germany
        {'latitude': -34.6037, 'longitude': -58.3816},  # Buenos Aires, Argentina
        {'latitude': 37.7749, 'longitude': -122.4194},  # San Francisco, USA
        {'latitude': 1.3521, 'longitude': 103.8198},    # Singapore
        {'latitude': 41.8781, 'longitude': -87.6298},   # Chicago, USA
        {'latitude': 31.2304, 'longitude': 121.4737},   # Shanghai, China
        {'latitude': 59.3293, 'longitude': 18.0686},    # Stockholm, Sweden
        {'latitude': -26.2041, 'longitude': 28.0473},   # Johannesburg, South Africa
        {'latitude': 45.4215, 'longitude': -75.6919},   # Ottawa, Canada
        {'latitude': 25.2048, 'longitude': 55.2708},    # Dubai, UAE
        {'latitude': 30.0444, 'longitude': 31.2357},    # Cairo, Egypt
        {'latitude': 41.9028, 'longitude': 12.4964},    # Rome, Italy
        {'latitude': 50.4501, 'longitude': 30.5234},    # Kyiv, Ukraine
        {'latitude': -33.9249, 'longitude': 18.4241},   # Cape Town, South Africa
        {'latitude': 14.5995, 'longitude': 120.9842},   # Manila, Philippines
        {'latitude': 13.7563, 'longitude': 100.5018},   # Bangkok, Thailand
        {'latitude': 35.6897, 'longitude': 51.3890},    # Tehran, Iran
        {'latitude': 37.9838, 'longitude': 23.7275},    # Athens, Greece
        # (70 more locations to be added to meet 100 locations requirement)
    ]
    return random.choice(locations)


# Function to send a request and render JavaScript with retries
def send_request_and_render(url, playwright, retries=3):
    for attempt in range(retries):
        try:
            geolocation = get_random_geolocation()
            user_agent = get_random_user_agent()
            referrer = get_random_referrer()
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(user_agent=user_agent, geolocation=geolocation, permissions=['geolocation'])
            page = context.new_page()
            page.set_extra_http_headers({'Referer': referrer})
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            if page.is_navigating():
                page.wait_for_load_state("networkidle")
            print(f"Page title: {page.title()}, Geolocation: {geolocation}, User-Agent: {user_agent}, Referrer: {referrer}")
            return page
        except Exception as e:
            print(f"Request attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(5)

# Function to simulate additional interactions
def simulate_interactions(page):
    interaction_scripts = [
        "document.querySelector('a') && document.querySelector('a').click();",
        "document.querySelector('button') && document.querySelector('button').click();",
        "document.querySelector('input') && (document.querySelector('input').value = 'test');"
    ]
    try:
        for script in interaction_scripts:
            # Check if page is navigating and wait if necessary
            if page.is_navigating():
                page.wait_for_load_state("networkidle")
            page.evaluate(f"() => {{{script}}}")
        time.sleep(random.uniform(2, 5))  # Wait after interaction
    except Exception as e:
        print(f"Interaction simulation failed: {e}")


# Function to simulate traffic
def simulate_traffic(url):
    with sync_playwright() as playwright:
        while True:
            page = send_request_and_render(url, playwright)
            if page:
                try:
                    simulate_interactions(page)
                except Exception as e:
                    print(f"Interaction simulation failed: {e}")
                finally:
                    page.context.close()  # Close the context to ensure resources are released
            time.sleep(random.uniform(1, 5))

# Main function
if __name__ == "__main__":
    url = "https://www.highrevenuenetwork.com/iaqgtx69y1?key=14a1e46999747270c942f2634ef5306a"
    simulate_traffic(url)
