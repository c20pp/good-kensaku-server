import requests
import json
import csv

def main():
    with open('../data/feedback_prev.csv') as f:
        r = csv.reader(f,skipinitialspace=True)
        l = [row for row in r]
    l2 = []
    headers ={'Content-Type': 'application/json'}
    url = 'http://localhost:8080/api/filters'
    for v in l:
        urls = v[0]
        param = json.dumps({
            'urls': [urls,],
        })
        response = requests.post(url,param,headers=headers)
        result = json.loads(response.text)['results'][0]
        l2.append([v[0],v[1],result])
    with open('../data/feedback_next.csv',mode='w') as f:
        w = csv.writer(f)
        w.writerows(l)

if __name__=='__main__':
    main()