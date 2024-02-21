import json

"""
!!!!!BEFORE RUNNING THIS SCRIPT, REMOVE THE LAST COMMA FROM THE LAST CVE!!!!!
"""


# Inspiration Source: ChatGPT


def compare_cves_from_map(map_of_cves):
    similarity_map = {}
    checked_keys = set()

    # Now you can iterate over each key-value pair
    for key, value in map_of_cves.items():
        for comparison_key, comparison_value in map_of_cves.items():
            # do not run comparison on the same key, or if the key combination has already been checked
            if key != comparison_key and (key, comparison_key) not in checked_keys and (
                    comparison_key, key) not in checked_keys:
                checked_keys.add((key, comparison_key))

                a = set(value.split())
                b = set(comparison_value.split())
                c = a.intersection(b)

                percent_similarity = float(len(c)) / (len(a) + len(b) - len(c))

                if percent_similarity >= tolerance:
                    similarity_key = f"{key}//{comparison_key}"
                    similarity_map[similarity_key] = percent_similarity

                    print(f"Checking for similarities of {similarity_key}...   Found significant similarities.")
                else:
                    print(f"Checking for similarities of {key}//{comparison_key}...   Not similar enough.")

                print(similarity_map)

    print('COMPLETE')


def compare_cves_from_list(list_of_cves, starting_position):
    res_file = open("results.json", "a")

    # Now you can iterate over the list by index
    for i in range(starting_position, len(list_of_cves)):
        # this will only have 1 key-value pair, so not computationally intensive
        cve_map = list_of_cves[i]
        key = list(cve_map.keys())[0]
        value = list(cve_map.values())[0]

        # loop through all subsequent CVEs - this works because it is assumed that you have already checked
        # the current CVE against all previous CVEs in previous loops
        # this will be more computationally intensive upfront, and then become less intensive as the processing
        # moves farther through the list
        for i2 in range(i + 1, len(list_of_cves)):
            cve_map2 = list_of_cves[i2]
            comparison_key = list(cve_map2.keys())[0]
            comparison_value = list(cve_map2.values())[0]

            a = set(value.split())
            b = set(comparison_value.split())
            c = a.intersection(b)

            percent_similarity = float(len(c)) / (len(a) + len(b) - len(c))

            if percent_similarity >= tolerance:
                similarity_key = f"{key}//{comparison_key}"
                res_file.write(f"({similarity_key}, {percent_similarity})\n")

                print(f"Checking for similarities of {similarity_key}...   Found significant similarities.")
            else:
                print(f"Checking for similarities of {key}//{comparison_key}...   Not similar enough.")

        print('COMPLETE')

    res_file.close()


tolerance = 0.75  # update value with preferred tolerance level

file_name = "clean_cves_list_2014_2024.json"

cleansed_cves_file = open(file_name, 'r')
json_data = json.load(cleansed_cves_file)
cleansed_cves_file.close()

results_file = open("results.json", "w")
results_file.write("[\n")
results_file.close()

compare_cves_from_list(json_data, 0)

results_file = open("results.json", "a")
results_file.write("]")
results_file.close()
