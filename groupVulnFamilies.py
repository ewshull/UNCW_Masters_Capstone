import json

with open("compiledResultsAt90Perc.json", "r") as compiled_res:
    json_data = json.load(compiled_res)

outliers_map = {}
family_map = {}
skip_until_index = -1
for index in range(len(json_data)):
    if index < skip_until_index:
        continue

    data_list = json_data[index]

    key = data_list[0]
    val = data_list[1]

    similar_matches = 0
    for index_comparison in range(index + 1, len(json_data)):
        data_list_comparison = json_data[index_comparison]

        # key_comparison = data_list_comparison[0]
        val_comparison = data_list_comparison[1]

        if val == val_comparison:
            similar_matches += 1
        else:
            if similar_matches > 1000:
                outliers_map[key] = similar_matches

            if family_map.get(similar_matches) is None:
                family_map[similar_matches] = 0

            matches_found = family_map.get(similar_matches)

            matches_found += 1

            family_map[similar_matches] = matches_found

            skip_until_index = index_comparison

            print(f"Skipping until next index: {skip_until_index}")

            break

print('COMPLETE')
print(dict(sorted(family_map.items())))
print('OUTLIERS')
print(outliers_map)
