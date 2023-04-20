# Employee Database Management System

This is an employee database management system built using the Django web framework. The purpose of this project is to help organizations manage employee records efficiently.

## Features

- Employee records management
- Department records management
- User authentication
- User authorization
- User roles management
- Dashboard for quick view of employee and department records
- Export employee records to CSV file

## Requirements

- Python 3.x
- Django==4.2
- django-crispy-forms
- crispy-bootstrap4==2022.1
- django-crispy-forms==2.0
- django-session-timeout==0.1.0
- Pillow==9.5.0

## Installation

1. Clone the repository `git clone https://github.com/laminjawla1/yimf_hr`
2. Install the required packages using `pip install -r requirements.txt`
3. Run the database migrations using `python manage.py migrate`
4. Start the development server using `python manage.py runserver`

## Usage

1. Go to the URL `http://localhost:8000/` in your web browser
2. type on terminal `python manage.py createsuperuser`
3. Login using your credentials
4. Create departments and employees records as required
5. Export employee records as CSV file using the admin interface

## Contributing

If you want to contribute to this project, please follow these steps:

1. Fork this repository
2. Create a new branch for your feature or bug fix
3. Make your changes and test thoroughly
4. Submit a pull request to the master branch

## License

OpenSource
