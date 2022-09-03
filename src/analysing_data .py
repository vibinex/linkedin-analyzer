# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

import matplotlib.pyplot as plt

# %matplotlib inline

# %%
exp_data = pd.read_csv("/Users/inikaagarwal/PycharmProjects/linkedin-analyzer/data/iitk_experience_data50.csv")

# %%
edu_data = pd.read_csv("/Users/inikaagarwal/PycharmProjects/linkedin-analyzer/data/iitk_education_data50.csv")

# %%
exp_data['User id'].nunique()

# %%
df = exp_data.groupby('User id').head(2)

# %%
companies_plot = df['Companies'].value_counts().head(20).plot(kind='barh')
companies_plot.set_ylabel("Companies")
companies_plot.set_xlabel("Number of People")

# %%
job_titles_plot = df['Job Titles'].value_counts().head(20).plot(kind='barh')
job_titles_plot.set_ylabel("Job Titles")
job_titles_plot.set_xlabel("Number of People")

# %%
school_plot = edu_data['School Names'].value_counts().head(20).plot(kind='barh')
school_plot.set_ylabel("Schools")
school_plot.set_xlabel("Number of People")

# %%
df['Job Duration'] = df['Job Duration'].str.replace('yr','/')
df["Job Duration"] = df["Job Duration"].str.split("/").str.get(0)

# %%
df.loc[df['Job Duration'].str.contains('mo'), 'Job Duration'] = 0

# %%
convert_dict = {'Job Duration': int}  
df = df.astype(convert_dict)  

# %%
job_duration_plot = df['Job Duration'].sort_values(ascending=True).value_counts().plot(kind='barh')
job_duration_plot.set_ylabel("Job Duration (years)")
job_duration_plot.set_xlabel("Number of People")

# %%

edu_data['School Leaving Dates'] = edu_data['School Leaving Dates'].astype('Int64')
edu_data['School Joining Dates'] = edu_data['School Joining Dates'].astype('Int64')

school_leaving_year_plot = edu_data['School Leaving Dates'].value_counts().head(20).plot(kind='barh')
school_leaving_year_plot.set_ylabel("Scool Gradutaion Year")
school_leaving_year_plot.set_xlabel("Number of People")

# %%
