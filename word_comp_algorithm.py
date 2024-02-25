import json
import math

"""
!!!!!BEFORE RUNNING THIS SCRIPT, REMOVE THE LAST COMMA FROM THE LAST CVE!!!!!
"""


# Inspiration Source: ChatGPT

"""
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
    
    
def compare_cves_from_list(list_of_cves, starting_position, ending_position):
    res_file = open(f"(results_{starting_position}_{ending_position}.json", "w")
    res_file.write("[\n")

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
                res_file.write(f"(\'{similarity_key}\', {percent_similarity}),\n")

                print(f"Checking for similarities of {similarity_key}...   Found significant similarities.")
            else:
                print(f"Checking for similarities of {key}//{comparison_key}...   Not similar enough.")

        print('COMPLETE')

    res_file.write("]")
    res_file.close()
"""


def compute_intersection(list_of_cves):
    all_sets = {}
    for l in range(len(list_of_cves)):
        # this will only have 1 key-value pair, so not computationally intensive
        cve_map = list_of_cves[l]
        value = list(cve_map.values())[0]

        all_sets[l] = set(value.split())

    print(f"Completed the intersection of all records. Record count: {len(list(all_sets.values()))}")

    return all_sets


def compare_cves_from_list2(list_of_cves, map_of_intersections, starting_position, ending_position):
    res_file = open(f"results_rows_{starting_position}_{ending_position}.json", "w")
    res_file.write("[\n")

    # Now you can iterate over the list by index
    for i in range(starting_position, ending_position):
        cve_map = list_of_cves[i]
        key = list(cve_map.keys())[0]
        desc = list(map_of_intersections.values())[i]

        # loop through all subsequent CVEs - this works because it is assumed that you have already checked
        # the current CVE against all previous CVEs in previous loops
        # this will be more computationally intensive upfront, and then become less intensive as the processing
        # moves farther through the list
        for i2 in range(i + 1, len(list_of_cves)):
            cve_map2 = list_of_cves[i2]
            comparison_key = list(cve_map2.keys())[0]
            comparison_desc = list(map_of_intersections.values())[i2]

            c = map_of_intersections[i].intersection(map_of_intersections[i2])

            percent_similarity = len(c) / (len(desc) + len(comparison_desc) - len(c))

            if percent_similarity >= tolerance:
                similarity_key = f"{key}//{comparison_key}"
                res_file.write(f"(\'{similarity_key}\', {percent_similarity}),\n")

                print(f"Checking for similarities of {similarity_key}...   Found significant similarities.")
            else:
                print(f"Checking for similarities of {key}//{comparison_key}...   Not similar enough.")

        print('COMPLETE')

    res_file.write("]")
    res_file.close()


tolerance = 0.75  # update value with preferred tolerance level

file_name = "clean_cves_list_2014_2024.json"

cleansed_cves_file = open(file_name, 'r')
json_data = json.load(cleansed_cves_file)
cleansed_cves_file.close()

all_sets_split = compute_intersection(json_data)

start = 0
for r in range(1, (math.ceil(len(all_sets_split.keys()) / 10000) + 2) * 10000):
    if r == math.ceil(len(all_sets_split.keys()) / 10000):
        compare_cves_from_list2(json_data, all_sets_split, start, len(all_sets_split.keys()))
    else:
        compare_cves_from_list2(json_data, all_sets_split, start, 10000 * r)
        start += 10000