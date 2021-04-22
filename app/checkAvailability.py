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
        orig = time["time"]
        date = orig.split("T")[0]
        time = orig.split("T")[1]
        time = time.split(".")[0]
        formatted_times += date + " (" + time + "), "
    return formatted_times[:-1]

def format_appointment( appt ):
    '''Takes in a dictionary as input, returns
    string of items in list format'''
    output = ""
    output += "url: "
    output += appt["url"] + "<br>"
    output += "provider: "
    output += appt["provider"] + "<br>"
    output += "address: "
    if appt["address"] == None:
        output += "n/a<br>"
    else: 
        output += appt["address"] + "<br>"
    output += "postal code: "
    if appt["postal_code"] == None: 
        output += "n/a<br>"
    else:
        output += appt["postal_code"] + "<br>"
    output += "appointments: "
    output += format_appt_times(appt["appointments"]) + "<br>"
    output += "vaccine types: "
    if "unknown" in appt["appointment_vaccine_types"]: 
        output += "unknown<br>"
    else: 
        if "pfizer" in appt["appointment_vaccine_types"]: 
            output += "pfizer "
        if "moderna" in appt["appointment_vaccine_types"]: 
            output += "moderna "
        output += "<br>"
    output += "2nd dose only: "
    output += str(appt["appointments_available_2nd_dose_only"])
    return output

def format_results( appts ): 
    '''Takes in a list of dictionaries as input, formats
    all appointments and returns string''' 
    if appts == []:
        return "n/a"
    output = ""
    for appt in appts:
        output += format_appointment(appt)
        output += "<br><br>"
    return output