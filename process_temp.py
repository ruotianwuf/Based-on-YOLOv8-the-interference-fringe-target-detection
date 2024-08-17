import pandas as pd




def modify_temperature(temp):
    temp_str = str(temp)
    if len(temp_str) > 2:
        return temp_str[:2] + '.' + temp_str[2:]
    else:
        return temp_str

if __name__ == '__main__':
    # Load the CSV file
    file_path = 'output_temp_time.csv'
    data = pd.read_csv(file_path)
    # Apply the function to the 'Temp' column
    data['Modified_Temp'] = data['Temp'].apply(modify_temperature)

    # Display the first few rows to confirm the modification
    print(data.head())

    # Optionally, save the modified data to a new CSV file
    output_file_path = 'modified_output_temp_time.csv'
    data.to_csv(output_file_path, index=False)
