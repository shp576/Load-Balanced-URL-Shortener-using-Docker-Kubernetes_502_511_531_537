## Week 1: Build the URL Shortener in Docker

This folder contains the basic URL shortener service implemented in Python Flask and containerized using Docker.

## File Structure

```
week1/
├── app/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container definition
├── docker-compose.yml      # Docker compose for local testing
└── README.md               # Documentation
```

## How to Run

1. Build and start the containers:
   ```
   docker-compose up -d
   ```

2. Test the API:
   ```
   # Create a shortened URL
   curl -X POST -H "Content-Type: application/json" -d '{"url":"https://www.example.com"}' http://localhost:5000/shorten
   
   # Use the returned short URL in your browser to verify redirection
   ```

3. Stop the containers:
   ```
   docker-compose down
   ```