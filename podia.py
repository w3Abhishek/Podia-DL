import requests
from colorama import Fore, Back, Style
import time
from bs4 import BeautifulSoup
import json

print(Fore.CYAN+"""
██████╗░░█████╗░██████╗░██╗░█████╗░░░░░░░██████╗░██╗░░░░░
██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗░░░░░░██╔══██╗██║░░░░░
██████╔╝██║░░██║██║░░██║██║███████║█████╗██║░░██║██║░░░░░
██╔═══╝░██║░░██║██║░░██║██║██╔══██║╚════╝██║░░██║██║░░░░░
██║░░░░░╚█████╔╝██████╔╝██║██║░░██║░░░░░░██████╔╝███████╗
╚═╝░░░░░░╚════╝░╚═════╝░╚═╝╚═╝░░╚═╝░░░░░░╚═════╝░╚══════╝"""+Style.RESET_ALL)

print(Fore.GREEN+"Created by Abhishek Verma (@w3Abhishek)"+Style.RESET_ALL,Fore.YELLOW+"\nReport all issues: https://github.com/w3Abhishek/Podia-DL"+Style.RESET_ALL)

course_website = str(input("Enter your Podia Course website:"))

r = requests.Session()

print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
print("░░░░░░ Login to Your Account ░░░░░░")
print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")

email = str(input("Enter the email: "))
password = str(input("Enter the password: "))

print("")

def authenticate(username, password):
	login_page = r.get(f"{course_website}/login").content
	soup = BeautifulSoup(login_page, "html.parser")
	code = soup.find("input", {"name": "authenticity_token"})['value']
	data = {
    'authenticity_token': code,
    'email': email,
    'password': password,
	}
	verification = r.post(f"{course_website}/sessions", data=data)
	print("Sending the verification email.\nPlease wait for 5 seconds.")
	otp = int(input("Enter the OTP you receieved on entered email: "))
	verification_page = r.get(verification.url).content
	soup = BeautifulSoup(verification_page, "html.parser")
	auth_token = soup.find("input", {"name":"authenticity_token"})['value']
	data = {
    'authenticity_token': auth_token,
    'session_verification_attempt[user_email]': email,
    'session_verification_attempt[code]': otp,
    'session_verification_attempt[trust_device]': '1',
	}
	course_page = r.post(f"{course_website}/session_verification", data=data)
	print("Authentication Completed!\n\nNow You're ready to download Podia Courses.")
	with open('podia_headers.json', 'w') as f:
	    json.dump(dict(course_page.headers), f)
	with open('podia_cookies.json', 'w') as f:
	    json.dump(dict(course_page.cookies), f)
	print("Podia session stored permanently.")
	return 200
authenticate(email, password)