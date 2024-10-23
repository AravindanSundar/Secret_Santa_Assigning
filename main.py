import pandas as pd

# File paths for CSV input and output
employee_list_csv_path = "Employee-List.csv"
previous_results_path = "Secret-Santa-Game-Result-2023.csv"

# Read CSV files
employee_list_csv = pd.read_csv(employee_list_csv_path)
print(employee_list_csv)

previous_results = pd.read_csv(previous_results_path)
print(previous_results)

# This is for merging employee list and previous results on Employee_Name
merged_data = pd.merge(employee_list_csv, previous_results[['Employee_Name', 'Secret_Child_Name']],
                       on='Employee_Name', how='left')


# This is a function to shuffle employees by their name and ensure no self-assignments or repeat assignments
def shuffle_employees(employee_list, previous_results):
    while True:
        shuffled_list = employee_list.sample(frac=1).reset_index(drop=True)

        conflict_found = False
        for i in range(len(employee_list)):  # Check line by line for conflicts
            if employee_list['Employee_Name'].iloc[i] == shuffled_list['Employee_Name'].iloc[i]:  # Check self-assignment
                conflict_found = True
                break

            if previous_results['Secret_Child_Name'].iloc[i] == shuffled_list['Employee_Name'].iloc[i]:  # Check for repeat assignments
                conflict_found = True
                break

        if not conflict_found:  # If no conflict is found, return the shuffled list
            return shuffled_list


shuffled_employee_list = shuffle_employees(employee_list_csv, merged_data)  # Shuffle employees until no conflicts

# Here we will assign secret children to the employee list
employee_list_csv['Secret_Child_Name'] = shuffled_employee_list['Employee_Name']
employee_list_csv['Secret_Child_EmailID'] = shuffled_employee_list['Employee_EmailID']

new_file_path = "Secret-Santa-Game-Result-2024.csv"
employee_list_csv.to_csv(new_file_path, index=False)
