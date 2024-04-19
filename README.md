## Setup Instructions

1. ## Clone the repository:
git clone [repository-url]

markdown
Copy code

2. ## Navigate into the directory:
cd [repository-directory]

markdown
Copy code

3. ## Edit the .env file with your MySQL credentials:

4. ## Build and run the Docker containers:
Example:
docker build -t user-management-service .
docker run -d -p 5001:5001 user-management-service
