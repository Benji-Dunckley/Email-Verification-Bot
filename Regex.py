import string
import random
import re

# Basic regex function to check if a word is in a message.
def checkMessage(word, message):
    checks = re.search(r"\b("+word+r")(s)?\b", message)
    if checks is not None:
        return True
    else:
        return False


# '' from above but now checks for email addresses.
def check_email(message):
    checks = re.search(r"\b[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*@+([a-zA-Z0-9]+\.)((ac)\.)(uk)", message)
    if checks is not None:
        return checks.group()
    else:
        return False


# Basic function to generate unique key
def generate_key():
    alpha = string.ascii_letters+string.digits
    return ''.join(random.choice(alpha) for i in range(20))
