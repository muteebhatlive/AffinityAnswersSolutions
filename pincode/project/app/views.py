from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AddressInputSerializer
import requests
from django.http import JsonResponse
import json
import re

@api_view(['POST'])
def pincode(request):
    if request.method == 'POST':    
        serializer = AddressInputSerializer(data=request.data)
        print('1')
        if serializer.is_valid():
            address = serializer.validated_data['address']
            # address_list = address.split()
            address_without_commas = address.replace(',', '')
            # Split the address by spaces
            address_list = address_without_commas.split()
            print('ADDRESS LIST: ',address_list)
            address_state = address_list[-2]
            print('ADDRESS_STATE', address_state)
            pincode = address_list[-1]
            print('PINCODE: ',pincode)
            if len(pincode) == 6 and isinstance(pincode, (int)):
                api_url = f'https://api.postalpincode.in/pincode/{pincode}'
                response = requests.get(api_url)
                if response.status_code == 200:
                    print(response)
                    json_data = response.json()
                    print('json_data: ', json_data)
                    status = json_data[0]["Status"]
                    if status == "Success":
                    # print('JSON: ',json_data)
                    # # print(type(json_data))
                        
                            
                        post_office_names = [post_office["Name"] for post_office in json_data[0]["PostOffice"]]
                        
                        post_data= {
                            "post_office_names": post_office_names
                        }
                        print('POST OFFICE NAME RESPONSE DATA: ', post_data)
                        
                        state_names = [state_name["State"] for state_name in json_data[0]["PostOffice"]]
                        
                        state_data = {
                            "state_names": state_names
                        }
                        print('STATE RESPONSE DATA: ', state_data)
                        
                        state_names_list = state_data.get('state_names')
                        post_names_list = post_data.get('post_office_names')
                        print(post_names_list)
                        
                        # Remove parentheses contents from each string encountered
                        cleaned_list = [re.sub(r'\([^)]*\)', '', value).strip() for value in post_names_list]

                        # Print the cleaned list
                        print(cleaned_list)
                        if address_state in state_names_list:
                            print('Address State Exists in the Pincode')
                            if any(keyword in post_names_list for keyword in address_list):
                                print("Post Office Match. Address corresponds to the pincode.")
                                print(address)
                                response_data = {
                                    "message" : "ADDRESS IS CORRECT",
                                    "address" : address
                                }

                                # Return the JSON response
                                return JsonResponse(response_data)
                            else:
                                print("Post Offices don't match")
                                response_data = {
                                            "message" : "ADDRESS IS INCORRECT",
                                            "address" : address
                                        }

                                        # Return the JSON response
                                return JsonResponse(response_data)
                        else:
                            print('Address State Does Not Exist in the Pincode')
                            response_data = {
                                            "message" : "ADDRESS IS INCORRECT",
                                            "address" : address
                                        }

                                        # Return the JSON response
                            return JsonResponse(response_data)
                    else:
                        error_message = json_data[0]["Message"]
                        return JsonResponse({"error": error_message}, status=400)
            
            else:
                response_data = {
                    "message" : "Invalid Pincode"
                }
            return JsonResponse(response_data, status=500)
                
        else:
            return JsonResponse({"error": "API request failed"}, status=500)
    
        