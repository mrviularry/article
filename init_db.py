import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection configuration
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Create User table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(120) NOT NULL,
        role VARCHAR(10) NOT NULL
    )
    ''')

    # Create Article table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS article (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(200) NOT NULL,
        content TEXT NOT NULL,
        slug VARCHAR(220) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL,
        company VARCHAR(100) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(id)
    )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
