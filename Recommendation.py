# Import tkinter for creating GUI elements
# Import ttk for themed widgets in the GUI
# Import pandas for data manipulation and analysis
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Load dataset
df = pd.read_csv('shopping_trends.csv')

# Set display options to show all rows and columns in the dataframe
pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  

# Function to recommend items based on selected color and category
def recommend_items_by_color_and_category():
    user_color = color_entry.get().strip().lower()
    user_category = category_entry.get().strip().lower()
    
    if not user_color or not user_category:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, "Please enter both color and category.")
        return
    
    filtered_items = df[(df['Color'].str.lower() == user_color) & 
                         (df['Category'].str.lower() == user_category)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for color '{user_color}' and category '{user_category}'.")
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, filtered_items[['Item Purchased', 'Color', 'Category']].to_string(index=False))

# Function to recommend items based on selected item and price range
def recommend_items_by_item_and_price_range():
    user_item = item_entry.get().strip()
    min_price = float(min_price_entry.get())
    max_price = float(max_price_entry.get())
    
    if not user_item:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, "Please enter an item to search.")
        return
    
    if min_price < 0 or max_price < 0:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, "Price values must be positive.")
        return
    
    if min_price > max_price:
        min_price, max_price = max_price, min_price
    
    filtered_items = df[(df['Item Purchased'].str.contains(user_item, case=False, na=False)) & 
                         (df['Purchase Amount (GBP)'] >= min_price) & 
                         (df['Purchase Amount (GBP)'] <= max_price)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for '{user_item}' in the price range between £{min_price} and £{max_price}.")
    else:
        sorted_items = filtered_items.sort_values(by='Purchase Amount (GBP)', ascending=True)
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, sorted_items[['Item Purchased', 'Purchase Amount (GBP)']].to_string(index=False))

# Function to recommend items based on selected gender and category
def recommend_items_by_gender_and_category():
    user_gender = gender_entry.get().strip().lower()  # Ensure case-insensitive matching
    user_category = category_entry_2.get().strip().lower()  # Ensure case-insensitive matching
    
    if not user_gender or not user_category:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, "Please enter both gender and category.")
        return
    
    filtered_items = df[(df['Gender'].str.lower() == user_gender) & 
                         (df['Category'].str.lower() == user_category)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for gender '{user_gender}' and category '{user_category}'.")
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, filtered_items[['Item Purchased', 'Gender', 'Category']].to_string(index=False))

# Function to recommend items based on selected item and size (exact match)
def recommend_items_by_item_and_size():
    user_item = item_size_entry.get().strip().lower()
    user_size = size_entry.get().strip().lower()

    filtered_items = df[(df['Item Purchased'].str.lower() == user_item) & 
                        (df['Size'].str.lower() == user_size)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for item '{user_item}' and size '{user_size}'.")
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, filtered_items[['Item Purchased', 'Size']].to_string(index=False))

# Function to recommend items based on selected item and review rating (high/low)
def recommend_items_by_item_and_rating():
    user_item = item_rating_entry.get().strip().lower()
    user_rating = rating_entry.get().strip().lower()

    filtered_items = df[df['Item Purchased'].str.contains(user_item, case=False, na=False)]

    if user_rating == 'high':
        filtered_items = filtered_items[filtered_items['Review Rating'] >= 4]
    elif user_rating == 'low':
        filtered_items = filtered_items[filtered_items['Review Rating'] < 4]
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, "Please choose either 'high' or 'low' for the review rating.")
        return

    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for item '{user_item}' with '{user_rating}' review rating.")
    else:
        sorted_items = filtered_items.sort_values(by='Review Rating', ascending=False if user_rating == 'high' else True)
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, sorted_items[['Item Purchased', 'Review Rating']].to_string(index=False))

# Function to recommend items based on user-selected item and age range
def recommend_items_by_item_and_age_range():
    user_item = item_age_entry.get().strip().lower()
    min_age = int(min_age_entry.get())
    max_age = int(max_age_entry.get())

    filtered_items = df[df['Item Purchased'].str.contains(user_item, case=False, na=False)]
    filtered_items = filtered_items[(filtered_items['Age'] >= min_age) & (filtered_items['Age'] <= max_age)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for item '{user_item}' and age range '{min_age}-{max_age}'.")
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, filtered_items[['Item Purchased', 'Age']].to_string(index=False))

# Function to recommend items based on selected category
def recommend_items_by_category():
    user_category = category_entry_3.get().strip().lower()
    filtered_items = df[df['Category'].str.lower() == user_category]
    
    result_text.delete(1.0, tk.END)  # Clear previous result
    result_text.insert(tk.END, filtered_items[['Item Purchased', 'Category']].to_string(index=False))

# Function to recommend items based on selected season
def recommend_items_by_season():
    user_season = season_entry.get().strip().lower()

    filtered_items = df[df['Season'].str.contains(user_season, case=False, na=False)]
    
    if filtered_items.empty:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, f"No items found for season '{user_season}'.")
    else:
        result_text.delete(1.0, tk.END)  # Clear previous result
        result_text.insert(tk.END, filtered_items[['Item Purchased', 'Season']].to_string(index=False))

# Function to recommend items based on selected color and item name
def recommend_items_by_color_and_name():
    user_color = color_name_entry.get().strip().lower()
    user_item_name = item_name_entry.get().strip().lower()

    filtered_items = df[ 
        (df['Color'].str.contains(user_color, case=False, na=False)) & 
        (df['Item Purchased'].str.contains(user_item_name, case=False, na=False))
    ]
    
    result_text.delete(1.0, tk.END)  # Clear previous result
    result_text.insert(tk.END, filtered_items[['Item Purchased', 'Color']].to_string(index=False))

# Create the main window
root = tk.Tk()
root.title("Item Recommendation System")

# Create frames for filters (left) and result (right)
filters_frame = tk.Frame(root)
filters_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

result_frame = tk.Frame(root)
result_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

# Color and Category Filter
color_label = tk.Label(filters_frame, text="Enter Color:")
color_entry = tk.Entry(filters_frame)
category_label = tk.Label(filters_frame, text="Enter Category:")
category_entry = tk.Entry(filters_frame)

color_category_button = tk.Button(filters_frame, text="Recommend by Color & Category", command=recommend_items_by_color_and_category)

color_label.grid(row=0, column=0)
color_entry.grid(row=0, column=1)
category_label.grid(row=1, column=0)
category_entry.grid(row=1, column=1)
color_category_button.grid(row=2, column=0, columnspan=2)

# Item and Price Filter
item_label = tk.Label(filters_frame, text="Enter Item Name:")
item_entry = tk.Entry(filters_frame)
min_price_label = tk.Label(filters_frame, text="Enter Min Price:")
min_price_entry = tk.Entry(filters_frame)
max_price_label = tk.Label(filters_frame, text="Enter Max Price:")
max_price_entry = tk.Entry(filters_frame)

item_price_button = tk.Button(filters_frame, text="Recommend by Item & Price", command=recommend_items_by_item_and_price_range)

item_label.grid(row=3, column=0)
item_entry.grid(row=3, column=1)
min_price_label.grid(row=4, column=0)
min_price_entry.grid(row=4, column=1)
max_price_label.grid(row=5, column=0)
max_price_entry.grid(row=5, column=1)
item_price_button.grid(row=6, column=0, columnspan=2)

# Gender and Category Filter
gender_label = tk.Label(filters_frame, text="Enter Gender:")
gender_entry = tk.Entry(filters_frame)
category_label_2 = tk.Label(filters_frame, text="Enter Category:")
category_entry_2 = tk.Entry(filters_frame)

gender_category_button = tk.Button(filters_frame, text="Recommend by Gender & Category", command=recommend_items_by_gender_and_category)

gender_label.grid(row=7, column=0)
gender_entry.grid(row=7, column=1)
category_label_2.grid(row=8, column=0)
category_entry_2.grid(row=8, column=1)
gender_category_button.grid(row=9, column=0, columnspan=2)

# Item and Size Filter
item_size_label = tk.Label(filters_frame, text="Enter Item Name:")
item_size_entry = tk.Entry(filters_frame)
size_label = tk.Label(filters_frame, text="Enter Size:")
size_entry = tk.Entry(filters_frame)

item_size_button = tk.Button(filters_frame, text="Recommend by Item & Size", command=recommend_items_by_item_and_size)

item_size_label.grid(row=10, column=0)
item_size_entry.grid(row=10, column=1)
size_label.grid(row=11, column=0)
size_entry.grid(row=11, column=1)
item_size_button.grid(row=12, column=0, columnspan=2)

# Item and Rating Filter
item_rating_label = tk.Label(filters_frame, text="Enter Item Name:")
item_rating_entry = tk.Entry(filters_frame)
rating_label = tk.Label(filters_frame, text="Enter Rating (high/low):")
rating_entry = tk.Entry(filters_frame)

item_rating_button = tk.Button(filters_frame, text="Recommend by Item & Rating", command=recommend_items_by_item_and_rating)

item_rating_label.grid(row=13, column=0)
item_rating_entry.grid(row=13, column=1)
rating_label.grid(row=14, column=0)
rating_entry.grid(row=14, column=1)
item_rating_button.grid(row=15, column=0, columnspan=2)

# Item and Age Filter
item_age_label = tk.Label(filters_frame, text="Enter Item Name:")
item_age_entry = tk.Entry(filters_frame)
min_age_label = tk.Label(filters_frame, text="Enter Min Age:")
min_age_entry = tk.Entry(filters_frame)
max_age_label = tk.Label(filters_frame, text="Enter Max Age:")
max_age_entry = tk.Entry(filters_frame)

item_age_button = tk.Button(filters_frame, text="Recommend by Item & Age", command=recommend_items_by_item_and_age_range)

item_age_label.grid(row=16, column=0)
item_age_entry.grid(row=16, column=1)
min_age_label.grid(row=17, column=0)
min_age_entry.grid(row=17, column=1)
max_age_label.grid(row=18, column=0)
max_age_entry.grid(row=18, column=1)
item_age_button.grid(row=19, column=0, columnspan=2)

# Category Filter
category_label_3 = tk.Label(filters_frame, text="Enter Category:")
category_entry_3 = tk.Entry(filters_frame)

category_button = tk.Button(filters_frame, text="Recommend by Category", command=recommend_items_by_category)

category_label_3.grid(row=20, column=0)
category_entry_3.grid(row=20, column=1)
category_button.grid(row=21, column=0, columnspan=2)

# Season Filter
season_label = tk.Label(filters_frame, text="Enter Season:")
season_entry = tk.Entry(filters_frame)

season_button = tk.Button(filters_frame, text="Recommend by Season", command=recommend_items_by_season)

season_label.grid(row=22, column=0)
season_entry.grid(row=22, column=1)
season_button.grid(row=23, column=0, columnspan=2)

# Color and Name Filter
color_name_label = tk.Label(filters_frame, text="Enter Color:")
color_name_entry = tk.Entry(filters_frame)
item_name_label = tk.Label(filters_frame, text="Enter Item Name:")
item_name_entry = tk.Entry(filters_frame)

color_name_button = tk.Button(filters_frame, text="Recommend by Color & Item", command=recommend_items_by_color_and_name)

color_name_label.grid(row=24, column=0)
color_name_entry.grid(row=24, column=1)
item_name_label.grid(row=25, column=0)
item_name_entry.grid(row=25, column=1)
color_name_button.grid(row=26, column=0, columnspan=2)

# Result Box with Scrollbar
result_text = tk.Text(result_frame, height=10, width=50)
result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
result_text.configure(yscrollcommand=result_scrollbar.set)

result_text.grid(row=0, column=0, sticky='nsew')
result_scrollbar.grid(row=0, column=1, sticky='ns')

result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

# Start the Tkinter event loop to make the GUI interactive
root.mainloop()