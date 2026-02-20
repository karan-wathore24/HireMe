# HireMe

HireMe is a modern recruitment platform connecting job seekers with top employers. Built with Python and Django, it facilitates a seamless hiring process with dedicated roles for HR professionals and candidates.

## Features

- **User Roles**: Distinct dashboards and functionalities for Job Seekers and Employers (HR).
- **Job Management**: Employers can post, manage, and track job listings.
- **Application Tracking**: Seekers can apply for jobs and track their application status.
- **Profile Management**:
  - **Seekers**: Upload resumes, list skills, and manage personal info.
  - **Employers**: Manage company profiles and contact details.
- **Search & Filter**: Powerful search functionality to find jobs by keyword, category, and location.
- **Responsive Design**: Fully responsive UI built with Bootstrap 5.

## Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite (Default)

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/HireMe.git
    cd HireMe
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access the application:**
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## License

This project is licensed under the MIT License.
