import json

batch_size = 1000
num_records = 165858

total_records = 0
for start in range(0, num_records, batch_size):
    end = min(start + batch_size, num_records)

    print(f"Writing results from: results_rows_{start}_{end}.json")

    with open(f"results_rows_{start}_{end}.json", "r") as one_res_file:
        json_data = json.load(one_res_file)

        print(f"Records found: {len(json_data)}")
        total_records += len(json_data)

        with open("compiledResultsAt90Perc.json", "a") as compiled_res_file:
            json.dump(json_data, compiled_res_file)

print(f"Total records found: {total_records}")
