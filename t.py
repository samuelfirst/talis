import re

command = '@talis_jtk hey'

at_ = re.match(r'\@(?P<username>(.+? ))', command)

print(at_['username'])
