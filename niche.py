from bs4 import BeautifulSoup
import requests
import json
import sqlite3 as sqlite
import plotly.plotly as py
import plotly.graph_objs as go

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    
    if unique_ident in CACHE_DICTION:
        #("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        #print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        #print("the problem might be here")
        return CACHE_DICTION[unique_ident]


DBNAME = 'schools.db'

def create_database():
    conn = sqlite.connect('schools.sqlite')
    cur = conn.cursor()

    statement = '''
            CREATE TABLE 'Names' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'UniversityName' TEXT,
                'State' TEXT NOT NULL,
                'Rank' INTEGER,
                'AcceptanceRate' INTEGER
                
            );
        '''
    cur.execute(statement)

    statement2 = '''
            CREATE TABLE 'NumberInfo' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'UniversityName' TEXT,
                'Students' INTEGER,
                'InStateTuition' INTEGER,
                'OutStateTuition' INTEGER
                
            );
        '''
    cur.execute(statement2)

user_input = 'ca rank'
splitting_input = user_input.split(" ")
state_name = splitting_input[0]
type_of_data = splitting_input[1]



def get_colleges_for_state(state):

    state_abbr_dict = {
        'ak': 'alaska',
        'al': 'alabama',
        'ar': 'arkansas',
        'az': 'arizona',
        'ca': 'california',
        'co': 'colorado',
        'ct': 'connecticut',
        'de': 'delaware',
        'fl': 'florida',
        'ga': 'georgia',
        'hi': 'hawaii',
        'ia': 'iowa',
        'id': 'idaho',
        'il': 'illinois',
        'in': 'indiana',
        'ks': 'kansas',
        'ky': 'kentucky',
        'la': 'louisiana',
        'ma': 'massachusetts',
        'md': 'maryland',
        'me': 'maine',
        'mi': 'michigan',
        'mn': 'minnesota',
        'mo': 'missouri',
        'ms': 'mississippi',
        'mt': 'montana',
        'nc': 'north-carolina',
        'nd': 'north-dakota',
        'ne': 'nebraska',
        'nh': 'new-hampshire',
        'nj': 'new-jersey',
        'nm': 'new-mexico',
        'nv': 'nevada',
        'ny': 'new-york',
        'oh': 'ohio',
        'ok': 'oklahoma',
        'or': 'oregon',
        'pa': 'pennsylvania',
        'ri': 'rhode-island',
        'sc': 'south-carolina',
        'sd': 'south-dakota',
        'tn': 'tennessee',
        'tx': 'texas',
        'ut': 'utah',
        'va': 'virginia',
        'vt': 'vermont',
        'wa': 'washington',
        'wi': 'wisconsin',
        'wv': 'west-virginia',
        'wy': 'wyoming'}

    state_from_abb = state_abbr_dict[state]







    baseurl = "https://www.niche.com/colleges/search/best-colleges/s/"
    states_page = baseurl + state_from_abb + "/"
    #page_text = make_request_using_cache(states_page)
    page_text = make_request_using_cache(states_page)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    #print(page_soup)

    content_div = page_soup.find(class_ = 'search-results')
    statename = content_div.find_all(class_ = 'search-results__list__item')
    #print(statename)

    #colleges_in_state = []
    #dictionary_of_schools = {}

    list_of_dictionaries = []


    for x in statename:
        
        try:
            dictionaries_of_school = {}

            getting_addy = x.find('a')['href']
            requesting_addy = make_request_using_cache(getting_addy)
            addy_soup = BeautifulSoup(requesting_addy, 'html.parser')
            #print(addy_soup)
            uni = addy_soup.find(class_ = "profile__bucket--1")
            unii = uni.find(class_ = "entity-name__link")
            unistr = str(unii)
            unispl = unistr.split('>')
            if "None" not in unispl[0]:
                unisplit = unispl[1].split("<")
                uni_name1 = unisplit[0]
                if "&amp;" in uni_name1:
                    uni_name11 = uni_name1.split("amp;")
                    nameee = ""
                    for z in uni_name11:
                        nameee += z
                    uni_name = nameee
                else:
                    uni_name = uni_name1



            rank = addy_soup.find(class_ = "rankings-statement")
            rankk = rank.find('strong')
            rankstr = str(rankk)
            rankspl = rankstr.split("->")
            ranksplit = rankspl[1].split("<")
            uni_rank = ranksplit[0]


            accc = addy_soup.find(id = "admissions")
            accep = accc.find(class_ = "scalar__value")
            accepstr = str(accep)
            accepspl = accepstr.split("n>")
            accepsplit = accepspl[1].split("<")
            acceptance_rate = accepsplit[0]


            tui = addy_soup.find(id = "cost")
            tuit = tui.find(class_ = "expansion-link")
            getting_tuit = tuit.find('a')['href']
            requesting_tuit = make_request_using_cache(getting_tuit)
            tuit_soup = BeautifulSoup(requesting_tuit, 'html.parser')
            getting_sticker = tuit_soup.find(id = "sticker-price")

            getting_in_state = getting_sticker.find(class_ = "profile__bucket--1")
            getting_in_state1 = getting_in_state.find(class_ = "scalar__value")
            in_state_str = str(getting_in_state1)
            in_state_spl = in_state_str.split("n>")
            in_state_split = in_state_spl[1].split("<")
            in_state_tuition = in_state_split[0]
            
            getting_out_state = getting_sticker.find(class_ = "profile__bucket--2")
            getting_out_state1 = getting_out_state.find(class_ = "scalar__value")
            out_state_str = str(getting_out_state1)
            out_state_spl = out_state_str.split("n>")
            out_state_split = out_state_spl[1].split("<")
            out_state_tuition = out_state_split[0]
            #print(out_state_tuition)
            

            stu = addy_soup.find(id = "students")
            stud = stu.find(class_ = "scalar__value")
            studstr = str(stud)
            studspl = studstr.split("n>")
            studsplit = studspl[1].split("<")
            students = studsplit[0]

            dictionaries_of_school["uni_name"] = uni_name
            dictionaries_of_school["state"] = state_from_abb
            dictionaries_of_school["uni_rank"] = uni_rank
            dictionaries_of_school["acceptance_rate"] = acceptance_rate
            dictionaries_of_school["in_state_tuition"] = in_state_tuition
            dictionaries_of_school["out_state_tuition"] = out_state_tuition
            dictionaries_of_school["students"] = students

            list_of_dictionaries.append(dictionaries_of_school)


            #colleges_in_state.append([uni_name, uni_rank, acceptance_rate, students, in_state_tuition, out_state_tuition])
        
            #print(colleges_in_state)
            #print('Im trying')
            

            #print(uni_name, uni_rank, acceptance_rate, students, in_state_tuition, out_state_tuition)


        except:
            #print('Nothing is happening')
            pass

    #dictionary_of_schools[state] = colleges_in_state
    #print(dictionary_of_schools)

    with open('data.json', 'w') as outfile:
        json.dump(list_of_dictionaries, outfile)

    return(list_of_dictionaries)


#state = 'alabama'
def insert_data():
    conn = sqlite.connect('schools.sqlite')
    cur = conn.cursor()
    with open('data.json') as infoJson:
        reading = infoJson.read()
        getting_data = json.loads(reading)

        checking_state = 'SELECT "State" FROM NAMES'
        cur.execute(checking_state)
        listts = []
        for rows in cur:
            listts.append(str(rows))

            #print(rows)
        for row in getting_data:
            combo = "('" + row['state'] + "',)"
            #print(combo)
            if combo not in listts:
                #print('This is fucked')
                uname = row['uni_name']
                ustate = row['state']
                urank = int(row['uni_rank'])
                uaccept = row['acceptance_rate'][:-1]
                uinstate = row['in_state_tuition'][1:]
                uoutstate = row['out_state_tuition'][1:]
                ustudents = row['students']
            
                insertion = (None, uname, ustate, urank, uaccept)
                statement = 'INSERT INTO "Names" '
                statement += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                
                
                insertion2 = (None, uname, ustudents, uinstate, uoutstate)
                statement1 = 'INSERT INTO "NumberInfo" '
                statement1 += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement1, insertion2)
    conn.commit()
    conn.close()



def plotting(input_from_user):
    conn = sqlite.connect('schools.sqlite')
    cur = conn.cursor()
    splitting_input = input_from_user.split(" ")
    state_name = splitting_input[0]
    type_of_data = splitting_input[1]

    state_abbr_dict = {
        'ak': 'alaska',
        'al': 'alabama',
        'ar': 'arkansas',
        'az': 'arizona',
        'ca': 'california',
        'co': 'colorado',
        'ct': 'connecticut',
        'de': 'delaware',
        'fl': 'florida',
        'ga': 'georgia',
        'hi': 'hawaii',
        'ia': 'iowa',
        'id': 'idaho',
        'il': 'illinois',
        'in': 'indiana',
        'ks': 'kansas',
        'ky': 'kentucky',
        'la': 'louisiana',
        'ma': 'massachusetts',
        'md': 'maryland',
        'me': 'maine',
        'mi': 'michigan',
        'mn': 'minnesota',
        'mo': 'missouri',
        'ms': 'mississippi',
        'mt': 'montana',
        'nc': 'north-carolina',
        'nd': 'north-dakota',
        'ne': 'nebraska',
        'nh': 'new-hampshire',
        'nj': 'new-jersey',
        'nm': 'new-mexico',
        'nv': 'nevada',
        'ny': 'new-york',
        'oh': 'ohio',
        'ok': 'oklahoma',
        'or': 'oregon',
        'pa': 'pennsylvania',
        'ri': 'rhode-island',
        'sc': 'south-carolina',
        'sd': 'south-dakota',
        'tn': 'tennessee',
        'tx': 'texas',
        'ut': 'utah',
        'va': 'virginia',
        'vt': 'vermont',
        'wa': 'washington',
        'wi': 'wisconsin',
        'wv': 'west-virginia',
        'wy': 'wyoming'}

    state_from_abb = state_abbr_dict[state_name]

    #print(state_from_abb)
    if type_of_data == "rank":

        checking = 'SELECT "UniversityName", "Rank" FROM NAMES WHERE "STATE" = '
        checking += "'" + state_from_abb + "'"

        cur.execute(checking)
        uni_nameee = []
        uni_rankkk = []
        for x in cur:
            uni_nameee.append(x[0])
            uni_rankkk.append(x[1])

        trace = go.Table(
            header=dict(values=['University Name', 'University Rank']),
            cells=dict(values=[uni_nameee,
                           uni_rankkk]))

        data = [trace] 
        py.plot(data, filename = 'basic_table')


    if type_of_data == "students":
        checking = '''SELECT i.UniversityName, i.Students, n.Rank
                    FROM Names as n
                    JOIN NumberInfo as i
                    ON n.UniversityName = i.UniversityName
                    WHERE n.State = '''
        checking += "'" + state_from_abb + "'"

        cur.execute(checking)
        univ_name = []
        univ_students = []
        univ_rank = []
        for x in cur:
            univ_name.append(x[0])
            univ_rank.append(x[2])
            getting_number = str(x[1])
            if "," in getting_number:
                splitting_number = getting_number.split(",")
                new_number = ""
                for z in splitting_number:
                    new_number += z
                univ_students.append(int(new_number))
            else:
                univ_students.append(int(getting_number))

        text_info = []
        count = 0
        for y in univ_name:
            text_line = str(y) + " (" + str(univ_rank[count]) + ")"
            text_info.append(text_line)
            count += 1
        #print(text_info)

        x = univ_name
        y = univ_students

        data = [go.Bar(
                    x=text_info,
                    y=y,
                    text=y,
                    textposition = 'auto',
                    marker=dict(
                        color='rgb(158,202,225)',
                        line=dict(
                            color='rgb(8,48,107)',
                            width=1.0),
                    ),
                    opacity=1
                )]

        py.plot(data, filename='bar-direct-labels')


    if type_of_data == "tuition":
        checking = '''SELECT n.UniversityName, i.InStateTuition, i.OutStateTuition
                    FROM NumberInfo as i
                    JOIN Names as n
                    ON n.UniversityName = i.UniversityName
                    WHERE n.State = '''
        checking += "'" + state_from_abb + "'"

        cur.execute(checking)
        univ_name = []
        univ_in_tuition = []
        univ_out_tuition = []
        for x in cur:
            univ_name.append(x[0])
            #univ_rank.append(x[2])
            getting_number = str(x[1])
            if "," in getting_number:
                splitting_number = getting_number.split(",")
                new_number = ""
                for z in splitting_number:
                    new_number += z
                univ_in_tuition.append(int(new_number))

            getting_number1 = str(x[2])
            if "," in getting_number1:
                splitting_number = getting_number1.split(",")
                new_number = ""
                for z in splitting_number:
                    new_number += z
                univ_out_tuition.append(int(new_number))

        trace1 = go.Bar(
            x= univ_name,
            y=univ_in_tuition,
            name='In State Tuition'
        )
        trace2 = go.Bar(
            x=univ_name,
            y=univ_out_tuition,
            name='Out of State Tuition'
        )

        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='grouped-bar')

    if type_of_data == "acceptance":
        checking = '''SELECT UniversityName, AcceptanceRate
                        FROM Names
                        WHERE State = '''
        checking += "'" + state_from_abb + "'"

        cur.execute(checking)
        uni_name = []
        uni_acceptance = []
        for x in cur:
            uni_name.append(x[0])
            uni_acceptance.append(x[1])



        data = [go.Bar(
                x=uni_acceptance,
                y=uni_name,
                orientation = 'h'
                )]

    py.plot(data, filename='horizontal-bar')


def load_help_text():
    with open('help.txt') as f:
        return f.read()


def interactive_prompt():
    help_text = load_help_text()
    #create_database()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')

        if response == 'help':
            print(help_text)
            continue

        list_of_commands = ["rank", "tuition", "students", "acceptance"]
        state_abbr_list = [
        'ak','al','ar','az','ca','co','ct','de','fl','ga','hi','ia','id','il','in','ks','ky',
        'la','ma','md','me','mi','mn','mo','ms','mt','nc','nd','ne','nh','nj','nm','nv','ny',
        'oh','ok','or','pa','ri','sc','sd','tn','tx','ut','va','vt','wa','wi','wv','wy']

        if response != 'exit':
            response_split = response.split()
            state_name_input = response_split[0]
            data_type_input = response_split[1]
            if state_name_input not in state_abbr_list:
                print("I'm sorry. I don't recognize that request. Enter 'help' for help")
                continue
            if data_type_input not in list_of_commands:
                print("I'm sorry. I don't recognize that request. Enter 'help' for help")
                continue


        if response != 'exit':
            response_split = response.split()
            state_name_from_input = response_split[0]
            get_colleges_for_state(state_name_from_input)
            insert_data()
            plotting(response)


if __name__=="__main__":
    interactive_prompt()
