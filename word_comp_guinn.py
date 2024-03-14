import json


def compute_intersection(list_of_cves):
    all_sets = {}
    for idx, cve_map in enumerate(list_of_cves):
        value = list(cve_map.values())[0]
        all_sets[idx] = set(value.split())

    print(f"Completed the intersection of all records. Record count: {len(list(all_sets.values()))}")
    return all_sets


def compare_cves_from_list(list_of_cves, map_of_intersections, starting_position, ending_position, tolerance):
    res = []
    for i in range(starting_position, ending_position):
        cve_map = list_of_cves[i]
        key = list(cve_map.keys())[0]
        desc = map_of_intersections[i]

        for i2 in range(i + 1, len(list_of_cves)):
            cve_map2 = list_of_cves[i2]
            comparison_key = list(cve_map2.keys())[0]
            comparison_desc = map_of_intersections[i2]

            intersection = desc.intersection(comparison_desc)
            percent_similarity = len(intersection) / (len(desc) + len(comparison_desc) - len(intersection))

            if percent_similarity >= tolerance:
                similarity_key = f"{key}//{comparison_key}"
                res.append((similarity_key, percent_similarity))
                print(f"Checking for similarities of {similarity_key}...   Found significant similarities.")
            else:
                print(f"Checking for similarities of {key}//{comparison_key}...   Not similar enough.")

    return res


tolerance = 0.75  # update value with preferred tolerance level

file_name = "clean_cves_list_2014_2024.json"

with open(file_name, 'r') as cleansed_cves_file:
    json_data = json.load(cleansed_cves_file)

all_sets_split = compute_intersection(json_data)

batch_size = 1000
num_records = len(all_sets_split.keys())

total_records = 0
for start in range(0, num_records, batch_size):
    end = min(start + batch_size, num_records)
    result = compare_cves_from_list(json_data, all_sets_split, start, end, tolerance)
    with open(f"results_rows_{start}_{end}.json", "w") as res_file:
        json.dump(result, res_file)

    total_records += len(result)

print(f"Total similarities found: {total_records}")
