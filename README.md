# Collaborative-Whiteboard-

This project is a collaborative whiteboard application built using Python, socket programming, and Tkinter. It allows multiple users to collaborate on a shared canvas in real-time.

**Installation**
Before running the application, ensure you have OpenSSL installed on your system. If not, you can download it from the OpenSSL website and follow the installation instructions for your platform.

After installing OpenSSL, verify the installation by running the following command in your terminal or command prompt:
  openssl version

If OpenSSL is installed correctly, you should see the version information displayed.

Next, follow these steps to generate the necessary cryptographic materials:

Generate a private key:
  openssl genpkey -algorithm RSA -out server.key -aes256
Generate a certificate signing request (CSR):
  openssl req -new -key server.key -out server.csr
  This command will prompt you to enter information about your server. You can leave most fields blank or use default values.
Generate a self-signed certificate:
  openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

**Usage**
Clone this repository to your local machine:
  git clone https://github.com/your-username/collaborative-whiteboard.git
Navigate to the project directory:
  cd collaborative-whiteboard
Run the server:
  python server.py
Run the client:
  python client.py




