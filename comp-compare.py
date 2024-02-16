import pandas as pd
import streamlit as st


def main():
    st.set_page_config(page_title="Compare old/new comp search")
    st.header("Compare old/new comp search")

    xlsx_file, sheet_name_old_comp_search, sheet_name_new_comp_search = get_user_input()

    if all([xlsx_file, sheet_name_old_comp_search, sheet_name_new_comp_search]):
        if st.button("Start analysis"):
            with st.spinner(text="In progress..."):
                perform_analysis(
                    xlsx_file, sheet_name_old_comp_search, sheet_name_new_comp_search
                )


def get_user_input():
    xlsx_file = st.file_uploader("Upload an excel file", type="xlsx")
    sheet_name_old_comp_search = st.text_input("Sheet name of old comp search")
    sheet_name_new_comp_search = st.text_input("Sheet name of new comp search")
    return xlsx_file, sheet_name_old_comp_search, sheet_name_new_comp_search


def perform_analysis(xlsx_file, sheet_name_old_comp_search, sheet_name_new_comp_search):
    st.write("Analysis will be started")

    old_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_old_comp_search)
    old_df["Source ID"] = old_df["Source ID"].astype(str).str.replace("-", "")
    # Should I use only Old in New/Old column?
    old_cs_data_accepted = old_df[(old_df["New/Old"] == "Old")]
    # old_cs_data_accepted = old_df

    new_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_new_comp_search)
    merged_df_company_name = pd.merge(
        old_cs_data_accepted,
        new_df,
        left_on="Comparable Company",
        right_on="company_name",
        suffixes=("_old", "_new"),
        how="inner",
    )

    st.write("Same comps appears in new comp search")
    st.write(merged_df_company_name)

    accepted_company_names = merged_df_company_name["Comparable Company"]
    indices_of_accepted_company_names = []

    for accepted_company_name in accepted_company_names:
        indices = new_df.index[new_df["company_name"] == accepted_company_name].tolist()
        indices_of_accepted_company_names.extend(indices)

    st.write("Analysis results will be displayed here")
    st.write(
        f"{len(indices_of_accepted_company_names)} accepted companies in new comp search results position (identical company name) in length of new comp search result of {len(new_df)} and length of old comp search result of {len(old_df)} is",
        indices_of_accepted_company_names,
    )
    st.write(
        f"{round((len(indices_of_accepted_company_names)/len(old_df)) * 100, 2)}% of accepted comps from old comp search was appeared in new comp search"
    )


if __name__ == "__main__":
    main()
