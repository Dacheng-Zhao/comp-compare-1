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
    sheet_name_psg_bench_mark = 'PSG System Benchmark v24.02.16'
    st.write("Analysis will be started")

    psg_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_psg_bench_mark)
    analysis_row = psg_df[psg_df["Benchmark to compare"] == sheet_name_old_comp_search]
    analysis_row = analysis_row.iloc[0]
    old_comp_pool_size = analysis_row['Unnamed: 5']

    old_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_old_comp_search)
    old_df["Source ID"] = old_df["Source ID"].astype(str).str.replace("-", "")
    old_cs_data_accepted = old_df[(old_df["New/Old"] == "Old")]

    new_df = pd.read_excel(xlsx_file, sheet_name=sheet_name_new_comp_search)
    merged_df_company_name = pd.merge(
        old_cs_data_accepted,
        new_df,
        left_on="Comparable Company",
        right_on="company_name",
        suffixes=("_old", "_new"),
        how="inner",
    )

    accepted_company_names = merged_df_company_name["Comparable Company"]
    indices_of_accepted_company_names = []

    for accepted_company_name in accepted_company_names:
        indices = new_df.index[new_df["company_name"] == accepted_company_name].tolist()
        indices_of_accepted_company_names.extend(indices)

    st.write("Analysis results will be displayed here")
    st.write(
        f"{len(indices_of_accepted_company_names)} accepted companies in new comp search results position (identical company name) in length of new comp search result of {len(new_df)} is",
        indices_of_accepted_company_names,
    )
    st.write("We have the table of comps that displays the comps that appear in both the old and new searches")
    st.write(merged_df_company_name)
    st.write(f"There are a total of {len(merged_df_company_name)} comps which are 'accepted' in both old and new searches")
    st.write(f"The pool size for the new search is {len(new_df)}")
    st.write(f"The pool size for the old search is {old_comp_pool_size}")
    st.write(f"There were {len(old_cs_data_accepted)} accepted comps in the old search")
    st.write(f"The % of accepted comps from the old search that show up in the new search is {round((len(merged_df_company_name)/len(old_cs_data_accepted)) * 100, 2)}%")


if __name__ == "__main__":
    main()