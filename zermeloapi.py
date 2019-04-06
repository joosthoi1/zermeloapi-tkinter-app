import requests, json
import os
import time, datetime

class Zapi:
    def __init__(self, school='', token='', useold=True):
        self.url = ('https://%s.zportal.nl/api/v3/' % school)
        self.token = token
        self.school = school
        self.useold = useold
        self.session = requests.Session()
        self.get_auth()

    def get_auth(self):
        if self.useold and os.path.isfile('token.json'):
            with open('token.json') as file:
                read1 = file.read()
                self.auth = json.loads(read1)["access_token"]
                self.school = json.loads(read1)["school"]
                self.url = ('https://%s.zportal.nl/api/v3/' % self.school)

        elif self.useold and not os.path.isfile('token.json'):

            token_response = self.session.post(self.url + 'oauth/token',  data={
            "grant_type": "authorization_code",
            "code":self.token.replace(' ','')
            })
            with open('token.json', 'w+') as file:
                try:
                    data = json.loads(token_response.text)
                except json.decoder.JSONDecodeError:
                    file.close()
                    print('School or code appears to be wrong or not valid')
                    os.remove('token.json')
                    return
                data['school'] = self.school
                file.write(json.dumps(data))
            self.auth = json.loads(token_response.text)["access_token"]

        else:
            self.session = requests.Session()
            token_response = self.session.post(self.url + 'oauth/token',  data={
            "grant_type": "authorization_code",
            "code":self.token.replace(' ','')
            })
            self.auth = json.loads(token_response.text)["access_token"]
    def get_users(self,user='',fields='prefix,lastName,code,schoolInSchoolYears,roles,firstName',flags='&isStudent=true&schoolInSchoolYear=751'):
        if user == '':
            response = self.session.get(f'{self.url}users?access_token={self.auth}{flags}&fields={fields}')
        else:
            response = self.session.get(f'{self.url}users?access_token={self.auth}{flags}&fields={fields}&code={user}')
        return(json.loads(response.text)['response']['data'])

    def schedule_week(self, user = '~me', fields = 'start,end,cancelled,remark,teachers,subjects,type,locations,moved,modified,valid', weeks=0):
        today = datetime.date.today()
        last_monday = today + datetime.timedelta(days=-today.weekday()+weeks*7)
        friday = today + datetime.timedelta(days=-today.weekday()+5+weeks*7)
        unix1= int(time.mktime(last_monday.timetuple()))
        unix2= int(time.mktime(friday.timetuple()))
#        print(unix1,unix2)
#        print(f'{self.url}appointments?access_token={self.auth}&start={unix1}&end={unix2}')

        if fields != '':
            response = self.session.get(f'{self.url}appointments?access_token={self.auth}&start={unix1}&end={unix2}&user={user}&fields={fields}')
        else:
            response = self.session.get(f'{self.url}appointments?access_token={self.auth}&start={unix1}&end={unix2}&user={user}')
        return json.loads(response.text)['response']['data']
    def del_token(self):
        os.remove('token.json')
#hey = Zapi('goudsewaarden')
#response = hey.schedule_week()
#print(response)
#zermelo = Zapi()
#users = zermelo.get_users('125977')
#print(users)
#for i in users['response']['data']:
#    print(i['firstName'], i['lastName'])
