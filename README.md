# Property Management System

This is a web application for managing properties. It is built with Django and Python.

## Features

- User management system with different roles (admin, customer)
- Property listing management (create, read, update, delete)
- Property details page with images, description, and location
- Customer dashboard to view and manage listings, reviews, and history
- Admin dashboard to manage users, properties, advertisements, and site settings
- Advertisement management system with different positions and activity status
- Subscription plans for customers to access premium features
- Contact us page with a form to send inquiries
- FAQ page with an accordion-style list of frequently asked questions
- Terms and Conditions page
- About Us page
- SEO optimization with customizable meta descriptions and keywords
- Integration with third-party libraries like Quill.js for rich text editing and Dropzone.js for file uploads
- Email notifications for contact form submissions and other events

## Installation

1. Clone the repository: `git clone `
2. Create a virtual environment: `poetry shell`
3. Install the dependencies: `poetry install`
4. Create the migrations: `python manage.py makemigrations`
5. Apply the migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## Usage

1. Access the admin dashboard at `/admin/`
2. Create or import property listings
3. Manage user accounts and permissions
4. Configure advertisement settings
5. Customize site settings, such as footer description

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License.
