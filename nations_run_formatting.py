import subprocess
import sys
import argparse
import os

# Function to install pandas
def install_pandas():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

try:
    import pandas as pd
except ImportError:
    print("Pandas is not installed. Installing now...")
    install_pandas()
    import pandas as pd

def main(input_file):
    # Read the CSV file
    df_nations_run = pd.read_csv(input_file)

    # Initialize a dictionary to store the transformed data
    runner_spender_dict = {
        'Laeufer_Name': [],   # Runner's name
        'Spender_Name': [],   # Donor's name
        'Spender_Mail': [],   # Donor's email
        'Spender_Runde': [],  # Amount per round
        'Spender_Hoechst': [], # Maximum amount
        'Spender_Fest': []      # Festbetrag
    }

    # Iterate over each row in the dataframe
    for index in range(len(df_nations_run)):
        # Combine 'Vorname' and 'Nachname' to form the full runner's name
        #laeufer_name = df_nations_run.loc[index]['Vorname'] + " " + df_nations_run.loc[index]['Nachname']
        
        # Split the 'Spenderliste' string into a list of individual donor entries
        spenders_per_runner = str(df_nations_run.loc[index]['Spenderliste']).split("\n")
        
        # Iterate over each donor entry
        for spender_per_runner in spenders_per_runner:
            # Split the donor entry into its details
            spender_details = spender_per_runner.split(", ")
            
            # Skip entries that don't have enough details
            if len(spender_details) < 2:
                continue
            
            # Append the details to the respective lists in the dictionary
            runner_spender_dict["Laeufer_Name"].append(df_nations_run.loc[index]['Name'])
            runner_spender_dict["Spender_Name"].append(spender_details[0].split(": ", 1)[1])
            runner_spender_dict["Spender_Mail"].append(spender_details[1].split(": ", 1)[1])
            runner_spender_dict["Spender_Runde"].append(spender_details[2].split(": ", 1)[1])
            runner_spender_dict["Spender_Hoechst"].append(spender_details[3].split(": ", 1)[1])
            runner_spender_dict["Spender_Fest"].append(spender_details[4].split(": ", 1)[1])

    # Create a DataFrame from the dictionary
    df_spender = pd.DataFrame.from_dict(runner_spender_dict)

    # Generate the output file name by adding '_formatted' suffix to the input file name
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_formatted.xlsx"

    # Save the DataFrame to an Excel file with the new name
    df_spender.to_excel(output_file, index=False)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Process Nations Run data.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    args = parser.parse_args()

    # Run the main function with the provided input file
    main(args.input_file)
