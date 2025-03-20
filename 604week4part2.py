#Scofield
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt 

# Read data
income_df = pd.read_excel('E:/web/2 week4/income.xlsx')
expenses_df = pd.read_csv('E:/web/2 week4/expenses.txt', sep=' ')

# Convert date format
income_df['Month'] = pd.to_datetime(income_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')
expenses_df['Month'] = pd.to_datetime(expenses_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')

# Check for invalid dates
if income_df['Month'].isna().any():
    print("Warning: Invalid dates found in income data.")
if expenses_df['Month'].isna().any():
    print("Warning: Invalid dates found in expenses data.")

# Merge data
merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')

# Calculate savings
merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']

# Check income and expenses
if merged_df['Income'].sum() <= 0:
    raise ValueError("Total income must be greater than zero.")
if merged_df['Expenses'].sum() > merged_df['Income'].sum():
    raise ValueError("Total expenses cannot exceed total income.")

# Calculate expense percentage
expense_percentage = merged_df['Expenses'].sum() / merged_df['Income'].sum() * 100
labels = ['Expenses', 'Savings']
sizes = [max(0, expense_percentage), max(0, 100 - expense_percentage)]

# Save to database
conn = sqlite3.connect('finance_data.db')
merged_df.to_sql('FinanceData', conn, if_exists='replace', index=False)

# Filter data that meets conditions
filtered_df = merged_df[(merged_df['Income'] > 7000) & (merged_df['Savings'] > 400)]
filtered_df.to_sql('FilteredFinanceData', conn, if_exists='replace', index=False)

conn.close()

# Plot charts
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Expense vs Savings Distribution')

plt.subplot(1, 2, 2)
merged_df.sort_values('Month', inplace=True)
merged_df.set_index('Month')['Savings'].plot(kind='line', marker='o', color='green')
plt.title('Monthly Savings Trends')
plt.xlabel('Month')
plt.ylabel('Savings ($)')

plt.tight_layout()
plt.show()