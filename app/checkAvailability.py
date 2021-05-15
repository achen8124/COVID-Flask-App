import requests
import string

def get_vacc_page( state ):
    """ This function requests the vaccine spotter page
        and reads in the input as a dictionary
    """
    vax_url = f"https://www.vaccinespotter.org/api/v0/states/{state}.json"
    result = requests.get(vax_url)
    if result.status_code == 200:
        data = result.json()
        return data          
    else:
        print("returning {}")
        return {"error": "State not found"}

def format_appt_info ( appt ): 
    """
    Takes in dictionary of appointment properties and deletes unnecessary fields 
    Returns dictionary storing appointment url, provider, address, postal code, 
    appointments, vaccine types, appointments available all doses, second dose only
    """
    new_appt = {}
    new_appt["url"] = appt["url"]
    new_appt["city"] = capitalize_string(appt["city"])
    new_appt["state"] = appt["state"]
    new_appt["provider"] = appt["provider"]
    new_appt["address"] = appt["address"]
    new_appt["postal_code"] = appt["postal_code"]
    new_appt["appointments"] = appt["appointments"]
    new_appt["appointments_available"] = appt["appointments_available"]
    new_appt["appointment_vaccine_types"] = appt["appointment_vaccine_types"]
    new_appt["appointments_available_all_doses"] = appt["appointments_available_all_doses"]
    new_appt["appointments_available_2nd_dose_only"] = appt["appointments_available_2nd_dose_only"]
    return new_appt

def get_vacc_by_city( city, state ):
    """
    Takes in desired city and state and returns list of available
    appointments
    """
    city = city.upper()
    appts_by_state = get_vacc_page(state)
    if "error" in appts_by_state:
        return []
    all_appts = appts_by_state["features"]
    available = []
    for feature in all_appts: 
        feature_city = feature["properties"]["city"]
        if (feature_city != None) and (feature_city.upper() == city) and \
            feature["properties"]["appointments_available"]:
            available.append(format_appt_info(feature["properties"]))
    return format_results( available )

def format_appt_times( times ):
    '''Takes in a list of appt times and formats them into string '''
    if times == []:
        return "n/a"
    formatted_times = ""
    for time in times: 
        if 'time' in time:
            orig = time["time"]
            date = orig.split("T")[0]
            time = orig.split("T")[1]
            time = time.split(".")[0]
            formatted_times += date + " (" + time + "), "
        else: 
            return "n/a"
    return formatted_times[:-1]

def format_provider( provider ):
    '''Takes in a string as input, replaces _ with a space and
    capitalizes the string'''
    if '_' in provider:
        words = [x.capitalize() for x in provider.split('_')]
        return " ".join(words)
    elif " " in provider:
        words = [x.capitalize() for x in provider.split()]
        return " ".join(words)
    elif provider == 'riteaid':
        return 'RiteAid'
    elif provider == 'cvs':
        return 'CVS'
    else:
        return provider.capitalize()

def capitalize_string( address ):
    '''Takes in a string as input, capitalizes the string'''
    words = [x.capitalize() for x in address.split()]
    return " ".join(words)

def format_appointment( appt ):
    '''Takes in a dictionary as input, returns
    string of items in list format'''
    output = ""
    output += "<h3>" + format_provider(appt["provider"]) + "</h3>"
    output += "<a href='"
    output += appt["url"] + "'>Click here for provider's website</a><br>"
    output += "Address: "
    if appt["address"] == None:
        output += "n/a<br>"
    else: 
        output += capitalize_string(appt["address"])
    if appt["city"] != None: 
        output += ", " + appt["city"] 
    if appt["state"] != None: 
        output += ", " + appt["state"]
    if appt["postal_code"] != None: 
        output += " " + appt["postal_code"] + "<br>"
    output += "Vaccine types: "
    if "unknown" in appt["appointment_vaccine_types"]: 
        output += "Unknown<br>"
    else: 
        if "pfizer" in appt["appointment_vaccine_types"]: 
            output += "Pfizer "
        if "moderna" in appt["appointment_vaccine_types"]: 
            output += "Moderna "
        output += "<br>"
    output += "Appointments:"
    times = format_appt_times(appt["appointments"])
    if times != "n/a":
        output += "<br><br>" + format_appt_table(times, appt["url"])
    else:
        output += " Please check the provider's website for more information!<br>"
    return output

def format_appt_table( appts, link ):
    '''Takes in a list of appointments and formats it in a HTML table,
    returns a string'''
    output = "<table><tr id='cols'>"
    times = appts.split(", ")
    used = {}
    hours = {'01':"1 AM", '02':"2 AM", '03':"3 AM", '04':"4 AM", '05':"5 AM", '06':"6 AM",
             '07':"7 AM", '08':"8 AM", '09':"9 AM", '10':"10 AM", '11':"11 AM", '12':"12 PM",
             '13':"1 PM", '14':"2 PM", '15':"3 PM", '16':"4 PM", '17':"5 PM", '18':"6 PM",
             '19':"7 PM", '20':"8 PM", '21':"9 PM", '22':"10 PM", '23':"11 PM", '24':"12 AM"}

    for appt in times:
        day = appt[:10]
        time = appt[12:17]
        if day not in used:
            used[day] = [time]
            output += "<th>" + day[5:].replace('-', '/') + "</th>"
        else:
            used[day] += [time]
    output += "</tr>"

    days = list(used.keys())
    empty = [False] * len(days)
    while not all(empty):
        output += "<tr>"
        for i in range(len(days)):
            if used[days[i]] == []:
                empty[i] = True
                output += "<td></td>"
            else:
                currTime = used[days[i]][0]
                hour = hours[currTime[:2]]
                minute = currTime[2:]
                hour_split = hour.split()

                finalTime = hour_split[0] + minute + " " +  hour_split[1]
                output += "<td><a href='" + link + "' id='time'>" + finalTime +"</a></td>"
                used[days[i]] = used[days[i]][1:]
        output += "</tr>"
    extra = 9 + 9 * len(days)
    output = output[:-extra]
    output += "</table>"
    return output


def format_results( appts ): 
    '''Takes in a list of dictionaries as input, formats
    all appointments and returns string''' 
    if appts == []:
        return "n/a"
    output = ""
    for appt in appts:
        output += "<div class='info'>"
        output += format_appointment(appt)
        output += "</div><br>"
    return output


def get_state( zipcode ): 
    '''
    Converts zipcode (int) to state abbreviation (string)
    '''
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