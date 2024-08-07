### README

# Article Deployer Application

This application allows users to deploy HTML articles while retaining the main website's header and footer. It includes admin and user functionalities, with users able to sign up and deploy HTML articles through a rich text editor. Articles are associated with user-provided name and company information, which are displayed when viewing the article.

## Features

- User registration and login
- Admin and user dashboards
- HTML article deployment with rich text editor
- Displaying articles with user's name and company information
- Edit and delete articles
- SQLite3 database support
- Responsive and modern UI design

## Setup Instructions

### Prerequisites

- Python 3.x
- Virtualenv

### Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   .\venv\Scripts\activate  # On Windows
   ```

3. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run database migration to ensure the database schema is updated:**
   ```sh
   python update_db.py
   ```

5. **Run the application:**
   ```sh
   python app.py
   ```

6. **Access the application:**
   Open your browser and go to `http://localhost:5000`.

### Uploading `memory.db` Remotely

To upload the `memory.db` file remotely, follow these steps:

1. **Ensure the remote server is configured to accept file uploads.**
2. **Upload the `memory.db` file to the server using a method such as SCP, SFTP, or a web-based file uploader.**

Example using SCP:
   ```sh
   scp memory.db user@remote_host:/path/to/destination
   ```

3. **Verify the `memory.db` file is in the correct location on the remote server.**

### Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```
SECRET_KEY=your_secret_key
```

Replace `your_secret_key` with a secure, random string.

## Usage

### User Registration and Login

- Navigate to the registration page to create a new user account.
- Login using the registered username and password.

### Deploying Articles

- Access the user dashboard.
- Click on "Deploy New Article".
- Fill in the article title, name, company, and content.
- Submit the form to deploy the article.

### Viewing Articles

- Articles can be viewed by clicking on the "View" link in the user dashboard.
- The article will display the title, company logo, and the name of the person who deployed it.

### Editing and Deleting Articles

- Articles can be edited or deleted from the user dashboard using the respective links.

## Admin Dashboard

- The admin can log in using the admin credentials.
- The admin dashboard allows viewing all articles deployed by all users.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
