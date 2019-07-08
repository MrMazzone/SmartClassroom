import requests

def classify(text):
    """
    This function will pass your text to the machine learning model and return the top result with the highest confidence
    """
    key = "***PASTE Your API Key HERE***"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


user_input = input("Tell me what to do?  ")

class_request = classify(user_input)

label = class_request["class_name"]
confidence = class_request["confidence"]

print ("result: '%s' with %d%% confidence" % (label, confidence))
