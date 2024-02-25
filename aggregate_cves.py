import requests
import json
import re
from unidecode import unidecode



def cleanse_data(file_open_type):
    raw_file = open("oldFiles/cves.json", 'r')
    raw_data = json.load(raw_file)
    raw_file.close()

    cleansed_cves_file = open("clean_cves_invalid.json", file_open_type)

    if file_open_type == "w":
        cleansed_cves_file.write("[\n")

    for cve in raw_data['vulnerabilities']:
        cve_id = cve['cve']['id']
        # cve_source = cve["cve"]["sourceIdentifier"]
        cve_desc = cve['cve']['descriptions'][0]['value']

        # escape meaningful or special characters
        cve_desc = str(cve_desc)
        cve_desc = unidecode(cve_desc)

        cve_desc = cve_desc.replace('\n', ' ').replace('\r', ' ').replace('	', ' ')

        cve_desc = cve_desc.replace('"', '\'').replace('\\', '/')

        cleansed_cves_file.write('{"' + str(cve_id) + '": "' + cve_desc + '"},\n')

        print("wrote CVE with Id: " + cve_id)

    cleansed_cves_file.close()


offset = 0
status_code = 200

while status_code == 200:
    # write (or overwrite) file contents
    original_file = open("oldFiles/cves.json", "w")

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0?noRejected&startIndex=" + str(offset)

    print("Starting.  Trying to contact NIST API for records at index " + str(offset) +
          " through " + str(offset + 2000) + "...")

    req = requests.get(url)

    status_code = req.status_code

    if status_code == 200:
        resp = json.loads(req.text)

        if resp['resultsPerPage'] != 0:
            print("SUCCESS FOR RECORDS " + str(offset) + " through " + str(offset + 2000))

            original_file.write(json.dumps(resp, indent=2))

            original_file.close()

            if offset == 0:
                cleanse_data("w")
            else:
                cleanse_data("a")

            offset += 2000
            print("Setting offset to " + str(offset))
        else:
            print("NO MORE RECORDS AT INDEX " + str(offset))

            cleansed_file = open("clean_cves_invalid.json", 'a')
            cleansed_file.write("]")
            cleansed_file.close()

            status_code = 500
    else:
        print("DID NOT WORK")

        original_file.close()
