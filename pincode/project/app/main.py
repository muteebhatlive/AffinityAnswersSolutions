import requests
def validate_pincode(address, pincode):
    api_url = f"https://api.postalpincode.in/pincode/{pincode}"
    
    try:
        response = requests.get(api_url)
        data = response.json()
        
        if response.status_code == 200 and data:
            for result in data:
                if result["PostOffice"]:
                    for office in result["PostOffice"]:
                        if address.lower() in office["Name"].lower():
                            return True
            return False
        else:
            return False

    except requests.exceptions.RequestException:
        return False

# Example usage
address = "2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka"
pincode = "560050"

if validate_pincode(address, pincode):
    print("PIN code matches the address.")
else:
    print("PIN code does not match the address.")