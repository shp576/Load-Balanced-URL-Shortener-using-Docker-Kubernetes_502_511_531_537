from locust import HttpUser, task, between
import random
import string

class URLShortenerUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.shortened_urls = []
    
    def generate_random_url(self):
        """Generate a random URL for testing"""
        domain = ''.join(random.choices(string.ascii_lowercase, k=10))
        path = ''.join(random.choices(string.ascii_lowercase, k=15))
        return f"https://{domain}.com/{path}"
    
    @task(3)
    def shorten_url(self):
        """Task to shorten a URL"""
        url = self.generate_random_url()
        response = self.client.post("/shorten", json={"url": url})
        
        if response.status_code == 201:
            data = response.json()
            short_url = data.get("short_url", "")
            if short_url:
                # Extract the short code from the full URL
                short_code = short_url.split("/")[-1]
                self.shortened_urls.append(short_code)
    
    @task(7)
    def access_short_url(self):
        """Task to access a shortened URL"""
        if self.shortened_urls:
            short_code = random.choice(self.shortened_urls)
            self.client.get(f"/{short_code}", allow_redirects=False)
        else:
            # If no shortened URLs yet, create one
            self.shorten_url()
    
    @task(1)
    def health_check(self):
        """Task to check the health endpoint"""
        self.client.get("/health")