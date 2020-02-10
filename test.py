import re
a ='https://i.pinimg.com/236x/0c/f5/88/0cf5884fae3f0c9dbf5569bf17491462.jpg'


print(re.search(pattern='(0-9a-z]*.jpg',string=a  ))



import os

      
if not os.path.exists('Pics'):
    os.mkdir('Pics')

query='dogs'
user_name='yuk'

if not os.path.exists('Pics/'+user_name+query):
    os.mkdir('Pics/'+user_name+'_'+query)

os.listdir('Pics')

[f for f in os.scandir() if f.is_dir()]

os.listdir('Pics/'+'yukunyang_gods')