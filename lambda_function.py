"""

Scheduled Auto-Scale for VMware Cloud on AWS

You can install python 3.6 from https://www.python.org/downloads/windows/

You can install the dependent python packages locally (handy for Lambda) with:
pip install requests -t . --upgrade
pip install configparser -t . --upgrade

"""

import requests                         # need this for Get/Post/Delete
import configparser                     # parsing config file
import time
import json

config = configparser.ConfigParser()
config.read("./config.ini")
strProdURL      = config.get("vmcConfig", "strProdURL")
strCSPProdURL   = config.get("vmcConfig", "strCSPProdURL")
Refresh_Token   = config.get("vmcConfig", "refresh_Token")
ORG_ID          = config.get("vmcConfig", "org_id")
SDDC_ID         = config.get("vmcConfig", "sddc_id")


print("The SDDC " + str(SDDC_ID) + " in the " + str(ORG_ID) + " ORG will be scaled down.")

def getAccessToken(myKey):
    params = {'refresh_token': myKey}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token

def removeCDChosts(hosts, org_id, sddc_id, sessiontoken):
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = strProdURL + "/vmc/api/orgs/" + org_id + "/sddcs/" + sddc_id + "/esxs"
    strRequest = {"num_hosts": hosts}
    response = requests.delete(myURL, json=strRequest, headers=myHeader)
    print(str(hosts) + " host(s) have been removed to the SDDC")
    print(response)
    return
   
# --------------------------------------------
# ---------------- Main ----------------------
# --------------------------------------------

def lambda_handler(event, context):
    session_token = getAccessToken(Refresh_Token)
    removeCDChosts(2, ORG_ID, SDDC_ID, session_token)
    return