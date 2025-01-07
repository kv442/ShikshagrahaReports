import streamlit as st
import pandas as pd

def process_csv(file):
    # Read the uploaded CSV file
    df = pd.read_csv(file)

    # Normalize column names (strip spaces and lowercase)
    df.columns = df.columns.str.strip().str.lower()

    # Required columns normalized
    required_columns = ['school name', 'question', 'question_response_label']
    normalized_required = [col.lower().replace(" ", "_") for col in required_columns]

    # Rename the dataframe columns to match normalized ones
    df.rename(columns=lambda col: col.strip().lower().replace(" ", "_"), inplace=True)

    # Check if the required columns exist
    if not all(col in df.columns for col in normalized_required):
        st.error(f"The uploaded CSV must contain the columns: {', '.join(required_columns)}")
        st.error(f"Detected columns: {', '.join(df.columns)}")
        return None

    # Pivot the data so each question becomes a column
    transformed_df = df.pivot_table(
        index='school_name', 
        columns='question', 
        values='question_response_label', 
        aggfunc='first'  # If multiple responses, take the first (can be adjusted)
    ).reset_index()

    # Flatten the column names
    transformed_df.columns.name = None

    return transformed_df

# Streamlit App
def main():
    st.title("Question Report Sheet Processor")

    st.write("Upload a CSV file to transform it based on 'School Name', 'question', and 'Question_response_label'.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Process the uploaded file
        transformed_data = process_csv(uploaded_file)

        if transformed_data is not None:
            st.write("## Transformed Data")
            st.dataframe(transformed_data)

            # Provide a download link for the transformed CSV
            csv = transformed_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Transformed CSV",
                data=csv,
                file_name="transformed_question_report.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
