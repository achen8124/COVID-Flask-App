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
        return {}

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
    all_appts = get_vacc_page( state )["features"]
    available = []
    for feature in all_appts: 
        feature_city = feature["properties"]["city"]
        if (feature_city != None) and (feature_city.upper() == city) and \
            feature["properties"]["appointments_available"]:
            available.append(format_appt_info(feature["properties"]))
    return available


# print(get_vacc_page( "CA" ))
print(get_vacc_by_city( "Claremont","CA" ))