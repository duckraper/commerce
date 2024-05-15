# Ecommerce Auction Site

## Description
This project is an eBay-style e-commerce auction site, developed solely with Django, HTML, and CSS, without the use of JavaScript. Bootstrap has been used for design, mostly. The site allows users to create, bid on, and view each of the auction listings, as well as enabling owners to manage each product. Users can also comment on each post, and views have been created for most web page functionalities. The validation system is ambiguous and is mainly implemented in the backend with Django, and is not responsive at all. This project is a response to project 2 of CS50w.

## Requirements
- Python
- Django
- Bootstrap

## Installation
1. Clone the repository: `git clone https://github.com/duckraper/commerce.git`
2. Navigate to the project directory: `cd commerce`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install the requirements: `pip install -r requirements.txt`
6. Perform database migrations: `python manage.py migrate`
7. Run the local server: `python manage.py runserver`
    - In case you want tu run the server in another host, then the default `localhost:8000` you need to modify the `commerce/settings.py`, then write in `ALLOWED_HOSTS` the hosts ip address you want to serve.

## Usage
1. Access the site through your web browser.
2. Register as a user or log in if you already have an account.
3. Explore the functionalities of creating, bidding, managing products, and commenting.

## Contribution
If you want to contribute to this project, hopefully in the client side,follow the steps below:
1. Fork the project
2. Create a new branch (`git checkout -b feature/contribution`)
3. Make your changes and commit them (`git commit -am 'Add your contribution'`)
4. Push the branch (`git push origin feature/contribution`)
5. Open a Pull Request

Hope you like it :)
