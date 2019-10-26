import json
import requests

key = 'a0a9effb69214daaabbbb216bc0782d4'

endpoint = 'https://junction2019.cognitiveservices.azure.com/text/analytics/v2.1/keyphrases'


def getKeyPhrases(description):

    documents = {"documents": [
        {"id": "1", "language": "en",
         "text": description},
    ]}

    headers = {"Ocp-Apim-Subscription-Key": key}
    response = requests.post(endpoint, headers=headers, json=documents)
    return response.json()


def checkProperties(input_dict, output_dict):
    for property in output_dict:
        if input_dict.get(property):
            output_dict[property] = input_dict[property]
    key_phrases = getKeyPhrases(output_dict["description"])
    key_phrases = key_phrases['documents'][0]['keyPhrases'] if key_phrases['documents'] else ""
    return key_phrases


def extract():

    with open('./yuri.json', 'r') as f:
        parsed_json = json.load(f)

    profile = {}



    #GENERAL
    general_properties = {
        "fullName": "",
        "headline": "",
        "company": "",
        "location": "",
        "description": ""
    }

    general_info = parsed_json["general"]

    key_phrases = checkProperties(general_info, general_properties)
    profile["general"] = []
    profile["general"].append({
        "fullName": general_properties["fullName"],
        "headline": general_properties["headline"],
        "company": general_properties["company"],
        "location": general_properties["location"],
        "keyPhrases": key_phrases
    })


    #JOBS
    job_properties = {
        "companyName": "",
        "jobTitle": "",
        "dateRange": "",
        "location": "",
        "description": ""
    }

    profile["jobs"] = []
    jobs = parsed_json["jobs"]
    for job in jobs:
        if job:
            key_phrases = checkProperties(job, job_properties)
            profile["jobs"].append({
                "companyName": job_properties["companyName"],
                "jobTitle": job_properties["jobTitle"],
                "dateRange": job_properties["dateRange"],
                "location": job_properties["location"],
                "keyPhrases": key_phrases
            })


    # SCHOOLS
    school_properties = {
        "schoolName": "",
        "degree": "",
        "degreeSpec": "",
        "dateRange": "",
        "description": ""
    }

    profile["schools"] = []
    schools = parsed_json["schools"]
    for school in schools:
        if school:
            key_phrases = checkProperties(school, school_properties)
            profile["schools"].append({
                "schoolName": school_properties["schoolName"],
                "degree": school_properties["degree"],
                "degreeSpec": school_properties["degreeSpec"],
                "dateRange": school_properties["dateRange"],
                "keyPhrases": key_phrases
            })

    profile["skills"] = []
    profile["skills"].append(parsed_json["skills"])

    with open('output.json', 'w') as outfile:
        json.dump(profile, outfile)


if __name__ == "__main__":
    extract()
