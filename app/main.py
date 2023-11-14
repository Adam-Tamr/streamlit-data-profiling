import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

def main():

    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
        st.image("Tamr-Logo.png")

    c1, c2 = st.columns(2)

    with c1:
        st.title("1. Is your data AI ready?")

        st.text(
            """
            Are you planning to unleash AI on your customer experience? 
            Answer a few questions and share a data sample to see if your 
            data quality can be trusted for AI-driven experiences."""
            )

        with st.form(key="data-questionnaire"):

            # Question 1
            entity_type = st.radio("1. What entity-type best describes your data?", ("People", "Companies"))
            # Question 2
            num_sources = st.number_input("2. How many data sources do you have?", min_value=1)
            # Question 3
            record_volume = st.number_input("3. What record volume do you have?", min_value=0, step=1)
            # Question 4
            num_attributes = st.number_input("4. How many attributes do you have?", min_value=1, step=1)
            # Question 5
            refresh_frequency = st.selectbox("5. How frequently is the data updated/refreshed?", ['In Realtime (seconds/minutes)','Daily', 'Weekly', 'Monthly', 'Yearly', 'Greater than yearly'])

            submitted = st.form_submit_button("Submit")

            # Build report from answers

            # Variety
            if num_sources == 1:
                variety_score = "C"
            elif num_sources >1 and num_sources <= 3:
                variety_score = "B"
            elif num_sources > 3:
                variety_score = "A+"

            # Volume
            if record_volume < 10000:
                volume_score = "C"
            elif record_volume >= 10000 and record_volume < 100000:
                volume_score = "B"
            elif record_volume >= 100000 and record_volume < 1000000:
                volume_score = "A"
            elif record_volume >= 1000000:
                volume_score = "A+"

            # Attributes
            if num_attributes < 10:
                breadth_score = "C"
            elif num_attributes >= 10 and num_attributes < 25:
                breadth_score = "B"
            elif num_attributes >= 25 and num_attributes < 50:
                breadth_score = "A"
            elif num_attributes >= 50:
                breadth_score = "A+"

            # Timeliness
            if refresh_frequency in ['In Realtime (seconds/minutes)','Daily', 'Weekly']:
                timeliness_score = "A+"
            elif refresh_frequency in [ 'Monthly']:
                timeliness_score = "B"
            elif refresh_frequency in ['Yearly', 'Greater than yearly']:
                timeliness_score = "C"




            if submitted:

                st.header(body = "Data Report Card", divider = 'blue')

                # Build report card from answers
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Variety", variety_score)
                with col2:
                    st.metric("Volume", volume_score)
                with col3:
                    st.metric("Breadth", breadth_score)
                with col4:
                    st.metric("Timeliness", timeliness_score)

    with c2:

        st.title("2. Upload a sample CSV for data quality analysis ")

        # Outside form
        # File Upload
        uploaded_file = st.file_uploader("Upload a sample CSV file and answer some clarifying questions", type=["csv"])

        # Check if a file is uploaded
        if uploaded_file is not None:

            # Read the uploaded file into a Pandas DataFrame
            df = pd.read_csv(uploaded_file)

            # Display a sample of the DataFrame
            st.write(df.head(5))
            st.caption("Data Sample")
                
            with st.form(key="data-profiling"):

                # Entity type
                data_entity_type = st.radio("1. What entity type best describes your data?", ("People", "Companies"))

                # Schema mapping
                company_name = st.selectbox(
                    label = "1. Please indicate which column (if any) contains Company Name information",
                    options = df.columns.tolist())
                
                address_line_1 = st.selectbox(
                    label = "2. Please indicate which column (if any) contains Address Line 1 information",
                    options = df.columns.tolist())
                
                email_phone = st.multiselect(
                    label = "3. Please indicate which column(s) (if any) contains Email or Phone information", 
                    options = df.columns.tolist())

                data_submitted = st.form_submit_button("Submit")


            # if data_submitted:
                # spinner = st.spinner('Building visualistions...')
                
                # with spinner:  
                #     # Top 10 companies
                #     if company_name is not None:
                #         top_companies = df[company_name].value_counts().head(10)
                #         st.text('Top 10 Companies by Frequency')
                #         st.bar_chart(top_companies)


                #     # Plot a bar chart of null counts
                #     null_counts = df.isnull().sum()

                #     fig, ax = plt.subplots()
                    
                #     null_counts.plot(kind='bar', color='#089FFF')
                #     ax.set_title('Null Count per Attribute')
                #     ax.set_xlabel('Attribute')
                #     ax.set_ylabel('Null Count')
                #     ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                #     st.pyplot(fig)                


                

            # # Check for missing values in each column
            # missing_values = df.isnull().sum()
            # st.write(f"Missing Values: {missing_values}")

            # # Calculate and display percentage of missing values for each column
            # missing_percentage = (missing_values / len(df)) * 100
            # st.write(f"Missing Percentage: {missing_percentage}")

            # # Display summary statistics for numerical columns
            # st.write("Summary Statistics:")
            # st.write(df.describe())

            # # Check attribute completeness (percentage of non-null values)
            # completeness = (df.count() / len(df)) * 100
            # st.write(f"Attribute Completeness: {completeness}")



if __name__ == "__main__":
    main()
