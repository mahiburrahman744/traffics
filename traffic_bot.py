import requests
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import time
import random
import sys

# URLs to fetch proxy lists
PROXY_URLS = {
    "socks5": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "socks4": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
    "http": "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
}

# Function to fetch proxies from URLs
def fetch_proxies():
    proxies = []
    for proxy_type, url in PROXY_URLS.items():
        response = requests.get(url)
        if response.status_code == 200:
            proxies.extend([f"{proxy_type}://{line.strip()}" for line in response.text.splitlines()])
    random.shuffle(proxies)
    return proxies

# Get the proxy list
proxy_list = fetch_proxies()

# Function to get a random proxy from the list
def get_random_proxy():
    if not proxy_list:
        raise Exception("Proxy list is empty")
    return proxy_list.pop()

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

# Function to send a request and render JavaScript with retries and rotating proxies
def send_request_and_render(url, playwright, retries=3):
    for attempt in range(retries):
        try:
            proxy = get_random_proxy()
            user_agent = get_random_user_agent()
            referrer = get_random_referrer()
            browser = playwright.chromium.launch(headless=True, proxy={"server": proxy})
            context = browser.new_context(user_agent=user_agent)
            page = context.new_page()
            page.set_extra_http_headers({'Referer': referrer})
            page.goto(url, timeout=60000)  # Set a longer timeout for navigation
            page.wait_for_load_state("networkidle")  # Wait for the page to load completely
            
            print(f"Page title: {page.title()}, Proxy: {proxy}, User-Agent: {user_agent}, Referrer: {referrer}")
            return page
        except Exception as e:
            print(f"Request attempt {attempt + 1} with proxy {proxy} failed: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(5)  # Wait before retrying

# Function to simulate scrolling
def simulate_scrolling(page):
    scroll_script = """
        var totalHeight = 0;
        var distance = 100;
        var scrollDown = true;
        var timer = setInterval(function() {
            var scrollHeight = document.body.scrollHeight;
            if (scrollDown) {
                window.scrollBy(0, distance);
                totalHeight += distance;
                if (totalHeight >= scrollHeight){
                    scrollDown = false;
                    totalHeight = 0;
                }
            } else {
                window.scrollBy(0, -distance);
                totalHeight += distance;
                if (totalHeight >= scrollHeight){
                    clearInterval(timer);
                }
            }
        }, 100);
    """
    try:
        page.evaluate(scroll_script)
        time.sleep(random.uniform(5, 10))  # Wait after scrolling down and up
    except Exception as e:
        print(f"Scrolling simulation failed: {e}")

# Function to simulate additional interactions
def simulate_interactions(page):
    interaction_scripts = [
        "document.querySelector('a') && document.querySelector('a').click();",
        "document.querySelector('button') && document.querySelector('button').click();",
        "document.querySelector('input') && (document.querySelector('input').value = 'test');"
    ]
    try:
        for script in interaction_scripts:
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
                simulate_scrolling(page)
                simulate_interactions(page)
                page.context.close()  # Close the context to ensure resources are released
            time.sleep(random.uniform(1, 5))

# Main function
if __name__ == "__main__":
    try:
        url = "https://www.highrevenuenetwork.com/iaqgtx69y1?key=14a1e46999747270c942f2634ef5306a"
        simulate_traffic(url)
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)
        sys.exit(1)
