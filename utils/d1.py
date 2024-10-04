import requests

BASE_URL = "https://d1-tutorial.rayhon1014.workers.dev/api/sources"

def get_sources():
    response = requests.get(BASE_URL)
    json = response.json()
    print(json)
    return json

def add_source(name, type, source, md_file, num_vectors):
    body = {
        "Name": name,
        "Type": type,
        "Source": source,
        "MD_File": md_file,
        "Num_Vectors": num_vectors
    }
    response = requests.post(BASE_URL, json=body)
    return response.json()

def delete_source(id):
    response = requests.delete(f"{BASE_URL}/{id}")
    return response.json()