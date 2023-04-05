#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# * As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending 645-675 per student actually underperformed compared to schools with smaller budgets (585 per student).
# 
# * As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).
# 
# * As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
# ---

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as py
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary

# In[2]:


# Calculate the total number of unique schools
school_count = len(school_data_complete['school_name'].unique())
school_count


# In[3]:


# Calculate the total number of students
student_count = len(school_data_complete['Student ID'].unique())
student_count


# In[4]:


school_data.head()


# In[5]:


student_data.head()


# In[6]:


# Calculate the total budget
total_budget = school_data['budget'].sum()
total_budget


# In[ ]:





# In[7]:


# Calculate the average (mean) math score
average_math_score = school_data_complete['math_score'].mean()
average_math_score


# In[8]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete['reading_score'].mean()
average_reading_score


# In[9]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[10]:


# Calculate the percentage of students who passeed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_complete[(school_data_complete['reading_score']>=70)].count()['student_name']
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[11]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[12]:


# passing_math_reading_count.shape


# In[13]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary =pd.DataFrame({
    'Total Students': [student_count],
    'Total Budget':[total_budget],
    'Average Math Score': [average_math_score],
    'Passing Math Percentage' : [passing_math_percentage],
    'Average Reading Score' : [average_reading_score],
    'Passing Reading Percentage' : [passing_reading_percentage],
    'Overall Passing Rate' : [overall_passing_rate],
   
})

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary

# In[14]:


# Use the code provided to select the school type
school_types = school_data.set_index(["school_name"])["type"]


# In[15]:


# Calculate the total student count
per_school_counts = school_data_complete['school_name'].value_counts()
per_school_counts.head()


# In[16]:


#Total number of students
school_data_complete.head()


# In[17]:


#Total schools budget
total_school_budget = school_data.set_index(['school_name'])['budget']
total_school_budget.head()


# In[18]:


# Calculate the total school budget and per capita spending
per_school_budget = school_data_complete.groupby(["school_name"]).mean()["budget"]
per_school_capita = per_school_budget / per_school_counts


# In[19]:


# school_data_complete.columns


# In[20]:


# Calculate the average test scores
per_school_math = school_data_complete.groupby(['school_name']).mean()['math_score']
per_school_reading = school_data_complete.groupby(['school_name']).mean()['reading_score']


# In[ ]:





# In[21]:


# Calculate the number of schools with math scores of 70 or higher
# school_passing_math = (per_school_math>=70).count()
school_passing_math = school_data_complete[(school_data_complete['math_score'] >= 70)]
# school_passing_math = school_passing_math['school_name'].value_counts()


# In[22]:


# Calculate the number of schools with reading scores of 70 or higher
# school_passing_reading = (per_school_reading>=70).count()
school_passing_reading = school_data_complete[(school_data_complete['reading_score'] >= 70)]
# school_passing_reading = school_passing_reading['school_name'].value_counts()


# In[23]:


# Use the provided code to calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
# passing_math_and_reading= passing_math_and_reading['school_name'].value_counts()


# In[24]:


# Use the provided code to calculate the passing rates
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100


# In[25]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary =pd.DataFrame({
    'School Types': school_types,
    'Students Per School':per_school_counts,
    'Total School Budget': total_school_budget,
    'Per Student Budget' : per_school_capita,
    'Average Math Score': per_school_math,
    '% Passing Math' : per_school_passing_math,
    'Average Reading Score': per_school_reading,
    '% Passing Reading' : per_school_passing_reading,
    '% Overall Passing' : overall_passing_rate,
   
})
#added this in to have a version of the school summaries from before the formatting
school_spending_df = per_school_summary.copy()
# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# In[26]:


per_school_summary.columns


# ## Highest-Performing Schools (by % Overall Passing)

# In[27]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=False)
top_schools.head(5)


# ## Bottom Performing Schools (By % Overall Passing)

# In[28]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by='% Overall Passing',ascending=True)
bottom_schools.head(5)


# ## Math Scores by Grade

# In[29]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(['school_name']).mean()
tenth_graders_scores = tenth_graders.groupby(['school_name']).mean()
eleventh_graders_scores = eleventh_graders.groupby(['school_name']).mean()
twelfth_graders_scores = twelfth_graders.groupby(['school_name']).mean()

# # Use the code to select only the `math_score`.
ninth_grade_math_scores = ninth_graders_scores['math_score']
tenth_grader_math_scores = tenth_graders_scores['math_score']
eleventh_grader_math_scores = eleventh_graders_scores['math_score']
twelfth_grader_math_scores = twelfth_graders_scores['math_score']

# # Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame({
    '9th Grade Math Average': ninth_grade_math_scores,
    '10th Grade Math Average':tenth_grader_math_scores,
    '11th Grade Math Average':ninth_grade_math_scores,
    '12th Grade Math Average':twelfth_grader_math_scores,
})

# # Minor data wrangling
math_scores_by_grade.index.name = None

# # Display the DataFrame
math_scores_by_grade.head()


# ## Reading Score by Grade 

# In[30]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(['school_name']).mean()
tenth_graders_scores = tenth_graders.groupby(['school_name']).mean()
eleventh_graders_scores = eleventh_graders.groupby(['school_name']).mean()
twelfth_graders_scores = twelfth_graders.groupby(['school_name']).mean()

# Use the code to select only the `reading_score`.
ninth_grade_reading_scores = ninth_graders_scores["reading_score"]
tenth_grader_reading_scores = tenth_graders_scores["reading_score"]
eleventh_grader_reading_scores = eleventh_graders_scores["reading_score"]
twelfth_grader_reading_scores = twelfth_graders_scores["reading_score"]

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({
    '9th Grade Reading Average': ninth_grade_reading_scores,
    '10th Grade Reading Average':tenth_grader_reading_scores,
    '11th Grade Reading Average':eleventh_grader_reading_scores,
    '12th Grade Reading Average':twelfth_grader_reading_scores,
})


# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[['9th Grade Reading Average', "10th Grade Reading Average", "11th Grade Reading Average", "12th Grade Reading Average"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade.head()


# ## Scores by School Spending

# In[31]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[32]:


# Create a copy of the school summary since it has the "Per Student Budget" 
# the there was some formatting added to the challenge when I received it ot convert
# the Per Student budget from a float to an object which didn't allow me to calculat anythin
# I moved the line of code to make a copy of the Per_School_Summary df to before the adjustments
# school_spending_df.info()


# In[33]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(school_spending_df['Per Student Budget'], bins=spending_bins, labels=labels)
school_spending_df.head()


# In[ ]:





# In[34]:


#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[35]:


# Assemble into DataFrame
spending_summary = pd.DataFrame({
    'Average Math Scores by Spending': spending_math_scores,
    'Average Reading Scores by Spending':spending_reading_scores,
    '% Passing Math by Spending':spending_passing_math,
    '% Passing Reading by Spending':spending_passing_reading,
    '% Passing Overall by Spending':overall_passing_spending,
})

# Display results
spending_summary


# ## Scores by School Size

# In[36]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
per_school_summary.columns


# In[37]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(school_spending_df['Students Per School'], bins=size_bins, labels=labels)
per_school_summary


# In[38]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
size_overall_passing = per_school_summary.groupby(["School Size"]).mean()["% Overall Passing"]


# In[41]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_summary = pd.DataFrame({
    'Average Math Scores by Size': size_math_scores,
    'Average Reading Scores by Size':size_reading_scores,
    '% Passing Math by Size':size_passing_math,
    '% Passing Reading by Size':size_passing_reading,
    '% Passing Overall by Size':size_overall_passing,
})

# Display results
# size_summary
per_school_summary.head()


# ## Scores by School Type

# In[43]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
type_math_scores = per_school_summary.groupby(["School Types"]).mean()["Average Math Score"]
type_reading_scores = per_school_summary.groupby(["School Types"]).mean()["Average Reading Score"]
type_passing_math = per_school_summary.groupby(["School Types"]).mean()["% Passing Math"]
type_passing_reading = per_school_summary.groupby(["School Types"]).mean()["% Passing Reading"]
type_overall_passing = per_school_summary.groupby(["School Types"]).mean()["% Overall Passing"]

# Use the code provided to select new column data
# average_math_score_by_type = type_math_scores["Average Math Score"]
# average_reading_score_by_type = type_reading_scores["Average Reading Score"]
# average_percent_passing_math_by_type = type_passing_math["% Passing Math"]
# average_percent_passing_reading_by_type = type_passing_reading["% Passing Reading"]
# average_percent_overall_passing_by_type = type_overall_passing["% Overall Passing"]


# In[44]:


# Assemble the new data by type into a DataFrame called `type_summary`
type_summary = pd.DataFrame({
    'Average Math Scores by Type': type_math_scores,
    'Average Reading Scores by Type':type_reading_scores,
    '% Passing Math by Type':type_passing_math,
    '% Passing Reading by Type':type_passing_reading,
    '% Passing Overall by Type':type_overall_passing,
})

# Display results
type_summary


# In[ ]:




