import streamlit as st
import pandas as pd

# Load the tab-delimited file into a DataFrame
file_path = r'C:\Users\Advali\Documents\food\extracted_texts.tsv'
df = pd.read_csv(file_path, delimiter='\t')

# Streamlit interface
st.title("Search PDF Extracted Texts")

# Text box for search input
search_text = st.text_input("Enter text to search (use semicolons to separate multiple keywords):")

if search_text:
    # Split the search text into multiple keywords
    keywords = [keyword.strip() for keyword in search_text.split(';') if keyword.strip()]

    if keywords:
        # Function to search and find snippets in the scanned text for a given keyword
        def search_snippets(row, keyword):
            lines = row['Scanned_text'].split('\n')
            snippets = [line for line in lines if keyword.lower() in line.lower()]
            return snippets

        # Initialize an empty list to store exploded DataFrames
        exploded_dfs = []

        # Apply the search function for each keyword and store the results in separate columns
        for idx, keyword in enumerate(keywords):
            col_name = f"Keyword{idx + 1}"
            df[col_name] = df.apply(lambda row: search_snippets(row, keyword), axis=1)
            # Explode the DataFrame for this keyword
            exploded_df = df[['Subdirectory', 'Filename', col_name]].explode(col_name)
            exploded_dfs.append(exploded_df.rename(columns={col_name: keyword}))

        # Merge all exploded DataFrames on 'Subdirectory' and 'Filename'
        final_results = exploded_dfs[0]
        for exploded_df in exploded_dfs[1:]:
            final_results = final_results.merge(exploded_df, on=['Subdirectory', 'Filename'], how='outer')

        # Filter out rows where all keyword columns are empty
        final_results = final_results.dropna(how='all', subset=keywords)

        if not final_results.empty:
            # Display the results
            st.write("Search Results:")
            st.table(final_results)
        else:
            st.write("No results found.")
    else:
        st.write("Please enter valid keywords separated by semicolons.")
