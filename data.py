from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import time
import secrets

#################################
########## Set up ###############
#################################
DB_NAME = 'final_project_DB.sqlite'
HEADER_1 = {'X-eBirdApiToken': secrets.API_KEY}
HEADER_2 = {'User-Agent': 'UMSI 507 Course Project - Python Scraping',
            'From': 'yiyixu@umich.edu',
            'Course-Info': 'https://si.umich.edu/programs/courses/507'}
PARAM = {'back': 30, 'maxResults': 10}
CACHE_FILE_NAME = 'final_project.json'
CACHE_DICT = {}


#################################
################ Class ##########
#################################
class Bird:
    '''a bird species
    Instance Attributes
    -------------------
    name: string
        the name of a bird species (e.g., Allen's Hummingbird)
    description: string
        description of bird
    '''
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Observation:
    def __init__(self, code, name, location, state, date, 
    amount, latitude, longitude):
        self.code = code
        self.name = name
        self.location = location
        self.state = state
        self.date = date
        self.amount = amount
        self.latitude = latitude
        self.longitude = longitude

#########################################
################ Caching ################
#########################################


def load_cache():
    ''' Load the dictionary for cache"
    Parameters
    ----------
    None
    Returns
    -------
    dict
        cache dictionary
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    ''' Save the cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    dict
        cache dictionary
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def parsing_using_cache(url):
    if url in CACHE_DICT.keys():
        return CACHE_DICT[url]
    else:
        resp = requests.get(url, headers=HEADER_2)
        CACHE_DICT[url] = resp.text
        save_cache(CACHE_DICT)
        return CACHE_DICT[url]


def json_using_cache(url):
    if url in CACHE_DICT.keys():
        return CACHE_DICT[url]
    else:
        resp = requests.get(url, headers=HEADER_1, params=PARAM)
        CACHE_DICT[url] = resp.json()
        save_cache(CACHE_DICT)
        return CACHE_DICT[url]




#########################################
################ Functions ##############
#########################################

states = {'Alabama': 'US-AL',
          'Alaska': 'US-AK',
          'Arizona': 'US-AZ',
          'Arkansas': 'US-AR',
          'California': 'US-CA',
          'Colorado': 'US-CO',
          'Connecticut': 'US-CT',
          'Delaware': 'US-DE',
          'Florida': 'US-FL',
          'Georgia': 'US-GA',
          'Hawaii': 'US-HI',
          'Idaho': 'US-ID',
          'Illinois': 'US-IL',
          'Indiana': 'US-IN',
          'Iowa': 'US-IA',
          'Kansas': 'US-KS',
          'Kentucky': 'US-KY',
          'Louisiana': 'US-LA',
          'Maine': 'US-ME',
          'Maryland': 'US-MD',
          'Massachusetts': 'US-MA',
          'Michigan': 'US-MI',
          'Minnesota': 'US-MN',
          'Mississippi': 'US-MS',
          'Missouri': 'US-MO',
          'Montana': 'US-MT',
          'Nebraska': 'US-NE',
          'Nevada': 'US-NV',
          'New Hampshire': 'US-NH',
          'New Jersey': 'US-NJ',
          'New Mexico': 'US-NM',
          'New York': 'US-NY',
          'North Carolina': 'US-NC',
          'North Dakota': 'US-ND',
          'Ohio': 'US-OH',
          'Oklahoma': 'US-OK',
          'Oregon': 'US-OR',
          'Pennsylvania': 'US-PA',
          'Rhode Island': 'US-RI',
          'South Carolina': 'US-SC',
          'South Dakota': 'US-SD',
          'Tennessee': 'US-TN',
          'Texas': 'US-TX',
          'Utah': 'US-UT',
          'Vermont': 'US-VT',
          'Virginia': 'US-VA',
          'Washington': 'US-WA',
          'West Virginia': 'US-WV',
          'Wisconsin': 'US-WI',
          'Wyoming': 'US-WY'}  




def get_obs_by_state():
    base = 'https://api.ebird.org/v2/data/obs/'
    extend = '/recent'
    l = []
    for k, v in states.items():
        url = base + v + extend
        resp = json_using_cache(url)
        for item in resp:
            try:
                code = item['speciesCode']
                name = item['comName']
                location = item['locName']
                state = k
                date = item['obsDt']
                amount = item['howMany']
                latitude = item['lat']
                longitude = item['lng']
            except KeyError:
                pass
            obs = Observation(code, name, location, state, date, amount, latitude, longitude)
            l.append(obs)
    return l 

def unique_species():
    l = []
    for item in get_obs_by_state():
        if item.code not in l:
            l.append(item.code)
    return l

def get_birds_instances():
    l = []
    base = 'https://ebird.org/species/'
    for item in unique_species():
        extend = item
        url = base + extend
        resp = parsing_using_cache(url)
        soup = BeautifulSoup(resp, 'html.parser')
        name = soup.find('h1',class_='Media--hero-title').text
        description = soup.find('p', class_='u-stack-sm').text
        bird = Bird(name, description)
        l.append(bird)
    return l



#########################################
################ Databases ##############
#########################################
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    drop_obs_sql = 'DROP TABLE IF EXISTS "Obs"'
    drop_birds_sql = 'DROP TABLE IF EXISTS "Birds"'
    
    create_obs_sql = '''
        CREATE TABLE IF NOT EXISTS "Obs" (
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT, 
            "SpeciesCode" TEXT NOT NULL,
            "SpeciesName" TEXT NOT NULL, 
            "Location" TEXT,
            "State" TEXT NOT NULL,
            "Date" TEXT,
            "HowMany" INTEGER, 
            "Latitude" REAL, 
            "Longitude" REAL 
        )
    '''
    create_birds_sql = '''
        CREATE TABLE IF NOT EXISTS 'Birds'(
            'Name' TEXT PRIMARY KEY,
            'Description' TEXT NOT NULL
        )
    '''
    cur.execute(drop_obs_sql)
    cur.execute(drop_birds_sql)
    cur.execute(create_obs_sql)
    cur.execute(create_birds_sql)
    conn.commit()
    conn.close()


def load_obs(): 
    insert_obs_sql = '''
        INSERT INTO Obs
        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    l = get_obs_by_state()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for o in l:
        cur.execute(insert_obs_sql,
            [
                o.code,
                o.name,
                o.location, 
                o.state,
                o.date,
                o.amount,
                o.latitude,
                o.longitude
            ]
        )
    conn.commit()
    conn.close()

def load_birds():
    insert_birds_sql = '''
        INSERT INTO Birds
        VALUES (?, ?)
    '''
    l = get_birds_instances()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for b in l:
        cur.execute(insert_birds_sql,
            [
                b.name,
                b.description
            ]
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    _start_time = time.time()

    def tic():
        global _start_time
        _start_time = time.time()

    def tac():
        t_sec = time.time() - _start_time
        (t_min, t_sec) = divmod(t_sec, 60)
        (t_hour, t_min) = divmod(t_min, 60)
        print('Time passed {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec))

    tic()
    CACHE_DICT = load_cache()
    create_db()
    load_obs()
    load_birds()
    tac()



    


    






