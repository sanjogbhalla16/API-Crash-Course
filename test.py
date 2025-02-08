import requests
import json

response = requests.get('https://api.stackexchange.com/2.3/questions?order=asc&sort=month&site=stackoverflow')

#print(response.json()['items'][0]['title'])

for questions in response.json()['items']:
    if questions['answer_count'] != '1':
        print(questions['title'])
        print(questions['link'])
    else:
        print('No answers')
    print('\n')
