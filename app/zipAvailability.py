import checkAvailability
import requests
import string

def get_state( zipcode ): 
    if (zipcode >= 35000 and zipcode <= 36999) : 
        st = 'AL' 
    elif (zipcode >= 99500 and zipcode <= 99999) : 
        st = 'AK' 
    elif (zipcode >= 85000 and zipcode <= 86999) :
        st = 'AZ' 
    elif (zipcode >= 71600 and zipcode <= 72999) :
        st = 'AR' 
    elif (zipcode >= 90000 and zipcode <= 96699) :
        st = 'CA' 
    elif (zipcode >= 80000 and zipcode <= 81999) :
        st = 'CO' 
    elif ((zipcode >= 6000 and zipcode <= 6389) or (zipcode >= 6391 and zipcode <= 6999)) :
        st = 'CT' 
    elif (zipcode >= 19700 and zipcode <= 19999) :
        st = 'DE' 
    elif (zipcode >= 32000 and zipcode <= 34999) :
        st = 'FL' 
    elif ( (zipcode >= 30000 and zipcode <= 31999) or (zipcode >= 39800 and zipcode <= 39999) ) :
        st = 'GA' 
    elif (zipcode >= 96700 and zipcode <= 96999) :
        st = 'HI' 
    elif (zipcode >= 83200 and zipcode <= 83999) :
        st = 'ID' 
    elif (zipcode >= 60000 and zipcode <= 62999) :
        st = 'IL' 
    elif (zipcode >= 46000 and zipcode <= 47999) :
        st = 'IN' 
    elif (zipcode >= 50000 and zipcode <= 52999) :
        st = 'IA' 
    elif (zipcode >= 66000 and zipcode <= 67999) :
        st = 'KS' 
    elif (zipcode >= 40000 and zipcode <= 42999) :
        st = 'KY' 
    elif (zipcode >= 70000 and zipcode <= 71599) :
        st = 'LA' 
    elif (zipcode >= 3900 and zipcode <= 4999) :
        st = 'ME' 
    elif (zipcode >= 20600 and zipcode <= 21999) :
        st = 'MD' 
    elif ( (zipcode >= 1000 and zipcode <= 2799) or (zipcode == 5501) or (zipcode == 5544 )) :
        st = 'MA' 
    elif (zipcode >= 48000 and zipcode <= 49999) :
        st = 'MI' 
    elif (zipcode >= 55000 and zipcode <= 56899) :
        st = 'MN' 
    elif (zipcode >= 38600 and zipcode <= 39999) :
        st = 'MS' 
    elif (zipcode >= 63000 and zipcode <= 65999) :
        st = 'MO' 
    elif (zipcode >= 59000 and zipcode <= 59999) :
        st = 'MT' 
    elif (zipcode >= 27000 and zipcode <= 28999) :
        st = 'NC' 
    elif (zipcode >= 58000 and zipcode <= 58999) :
        st = 'ND' 
    elif (zipcode >= 68000 and zipcode <= 69999) :
        st = 'NE' 
    elif (zipcode >= 88900 and zipcode <= 89999) :
        st = 'NV' 
    elif (zipcode >= 3000 and zipcode <= 3899) :
        st = 'NH' 
    elif (zipcode >= 7000 and zipcode <= 8999) :
        st = 'NJ' 
    elif (zipcode >= 87000 and zipcode <= 88499) :
        st = 'NM' 
    elif ( (zipcode >= 10000 and zipcode <= 14999) or (zipcode == 6390) or (zipcode == 501) or (zipcode == 544) ) :
        st = 'NY' 
    elif (zipcode >= 43000 and zipcode <= 45999) :
        st = 'OH' 
    elif ((zipcode >= 73000 and zipcode <= 73199) or (zipcode >= 73400 and zipcode <= 74999) ) :
        st = 'OK' 
    elif (zipcode >= 97000 and zipcode <= 97999) :
        st = 'OR' 
    elif (zipcode >= 15000 and zipcode <= 19699) :
        st = 'PA' 
    elif (zipcode >= 300 and zipcode <= 999) :
        st = 'PR' 
    elif (zipcode >= 2800 and zipcode <= 2999) :
        st = 'RI' 
    elif (zipcode >= 29000 and zipcode <= 29999) :
        st = 'SC' 
    elif (zipcode >= 57000 and zipcode <= 57999) :
        st = 'SD' 
    elif (zipcode >= 37000 and zipcode <= 38599) :
        st = 'TN' 
    elif ( (zipcode >= 75000 and zipcode <= 79999) or (zipcode >= 73301 and zipcode <= 73399) or  (zipcode >= 88500 and zipcode <= 88599) ) :
        st = 'TX' 
    elif (zipcode >= 84000 and zipcode <= 84999) :
        st = 'UT' 
    elif (zipcode >= 5000 and zipcode <= 5999) :
        st = 'VT' 
    elif ( (zipcode >= 20100 and zipcode <= 20199) or (zipcode >= 22000 and zipcode <= 24699) or (zipcode == 20598) ) :
        st = 'VA' 
    elif ( (zipcode >= 20000 and zipcode <= 20099) or (zipcode >= 20200 and zipcode <= 20599) or (zipcode >= 56900 and zipcode <= 56999) ) :
        st = 'DC' 
    elif (zipcode >= 98000 and zipcode <= 99499) :
        st = 'WA' 
    elif (zipcode >= 24700 and zipcode <= 26999) :
        st = 'WV' 
    elif (zipcode >= 53000 and zipcode <= 54999) :
        st = 'WI' 
    elif (zipcode >= 82000 and zipcode <= 83199) :
        st = 'WY' 
    else :
        st = 'none' 
    return st 
 

def get_vacc_by_zip( zip ):
    """
    Takes in desired zip code and state and returns list of available
    appointments
    """
    if len(zip) != 5:
          return "Invalid Zip Code"
    state = get_state(int(zip))
    appts_by_state = get_vacc_page(state)
    if "error" in appts_by_state:
          return []
    all_appts = appts_by_state["features"]
    available = []
    for feature in all_appts: 
          feature_zip = feature["properties"]["postal_code"]
          if (feature_zip != None) and (feature_zip == zip) and \
                feature["properties"]["appointments_available"]:
                available.append(format_appt_info(feature["properties"]))
    return format_results( available )