import modtran_analysis.tools.utils as utils
import pandas as pd
# This is creating all of the tables
sza_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
vza_bins = [0, 1, 2, 3, 4, 5, 6]
raa_bins = [0, 1, 2, 3, 4, 5, 6, 7]

data_files = list(range(1, 129))
missing = [10, 11, 41, 54, 55, 56, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122]
for i in range(len(missing)):
    data_files.remove(missing[i])


for data_file in data_files:
    all_results = []
    for s in sza_bins:
        for v in vza_bins:
            for r in raa_bins:
                # Call your function for each geometry
                v5_table_sample = utils.table_output(f"v5/FV3_Modtran6_IO_v5_scene_{data_files[data_file-1]}.nc", 'ERBE', r, s, v, 0)

                # Convert the dictionary to a single-row DataFrame
                import numpy as np
                flattened_table = np.squeeze(v5_table_sample)
                all_results.append(pd.DataFrame(flattened_table))
    # Combine all rows into one final table
    final_table_v5 = pd.concat(all_results, ignore_index=True)



    pd.option_context('display.max_rows',None, 'display.max_columns',None)
    final_table_v5.to_csv(f'/Users/kese6848/modtran_analysis/modtran_analysis/data/v5-tables/v5-table-{data_files[data_file-1]}.csv')


    # This is creating all of the summaries

    utils.table_summary(f'v5/FV3_Modtran6_IO_v5_scene_{data_files[data_file-1]}.nc', f'data/v5-tables/v5-table-{data_files[data_file-1]}.csv')
