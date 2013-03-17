#!/usr/bin/env python

import json
import requests

URL = "http://localhost:8890"
headers = {"Content-type" : "application/json"}

def main():
	r = requests.post(URL+"/user", headers=headers, data=json.dumps({"username":"zaar"}) )
	r.raise_for_status()
	print "Created user zaar", r.json()
	zid = r.json()["user_id"]

	r = requests.post(URL+"/user", headers=headers, data=json.dumps({"username":"kate"}) )
	r.raise_for_status()
	print "Created user kate", r.json()
	kid = r.json()["user_id"]

	r = requests.post(URL+"/friendship", headers=headers, data=json.dumps({"user_id":kid, "followed_user_id":zid}) )
	r.raise_for_status()
	print "Kate now follows Zaar", r.json()
	
	r = requests.post(URL+"/tweet", headers=headers, data=json.dumps({"user_id":zid, "text":"Hello World"}) )
	r.raise_for_status()
	print "Created tweet for zaar", r.json()

	r = requests.post(URL+"/tweet", headers=headers, data=json.dumps({"user_id":kid, "text":"Hello Zaar"}) )
	r.raise_for_status()
	print "Created tweet for kate", r.json()
	
	r = requests.get(URL+"/tweet", params={"user_id":zid})
	r.raise_for_status()
	print "zaar tweets:\n", r.json()
	
	r = requests.get(URL+"/tweet")
	r.raise_for_status()
	print "all tweets:\n", r.json()
	

if __name__ == "__main__":
	main()
