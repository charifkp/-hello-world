  # main(project)
from os.path import join
import timeit
import time
from functools import partial
import psutil, os
import gc
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from collections import Counter
import re
import numpy as np
import tracemalloc
import mmap
import os


#===========================================================================================🌍[start csv read]🌍======================================
def analyze_customer_purchase_volume(file_path, chunk_size=100000):
    """Analyzes customer purchase volume from a large CSV file in chunks."""
    customer_spending = pd.Series()
    customer_totals = {}
    try:
        for chunk in pd.read_csv(file_path, encoding="ISO-8859-1", chunksize=chunk_size):
            if 'CustomerID' in chunk.columns and 'Quantity' in chunk.columns and 'UnitPrice' in chunk.columns:
                chunk['TotalPrice'] = chunk['Quantity'] * chunk['UnitPrice']
                customer_chunk_totals = chunk.groupby('CustomerID')['TotalPrice'].sum()
                for customer_id, total_spent in customer_chunk_totals.items():
                    customer_totals[customer_id] = customer_totals.get(customer_id, 0) + total_spent
            elif 'CustomerID' in chunk.columns and 'TotalPrice' in chunk.columns:
                customer_chunk_totals = chunk.groupby('CustomerID')['TotalPrice'].sum()
                for customer_id, total_spent in customer_chunk_totals.items():
                    customer_totals[customer_id] = customer_totals.get(customer_id, 0) + total_spent
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred during customer analysis: {e}")
        return None

    if customer_totals:
        customer_spending = pd.Series(customer_totals).sort_values(ascending=False)
        return customer_spending
    return None
      #finc the key word of the data/บอกว่าลูกค้าเลขไหนซื้อสูงสุด
def read_csv(file_path):

    # [ start time of os read] ⏰
    start_time = time.time()
    mem_usage = get_memory_usage()
    # =========================⏰
    chunk_size = 100000
    print("===================================================================")
    print("-------------------------<chunk>-----------------------------------")
    print(f"First RAM usage: {psutil.virtual_memory().percent}%")

    try:

        lines = []
        chunk_reader = pd.read_csv(file_path, encoding="ISO-8859-1", chunksize=chunk_size)
        first_chunk = next(chunk_reader)
        for chunk in chunk_reader:
          textfilereader = chunk.astype(str).apply(lambda row: ','.join(row), axis=1).tolist()
          lines.extend(textfilereader)

# WHEN YOU WANT TO OUT PUT PART OF READ (CSV) PLASE COMMENT ONLY THIS HERE BELOW/ WHEN YOU WANT TO COMPARE PART JUST UNCOMMENT THAT OUT

        #  # [end time of os read]---⏰------------------------
        # end_time = time.time()
        # time_taken = end_time - start_time
        # memory_used = time_taken  - mem_usage
        # return lines, time_taken, memory_used
        # #-------------------------------⏰----------------



        print(f"Chunk size: {first_chunk.shape}")
        print(f"Processing DataFrame chunk with {len(first_chunk)} rows...")
        print(f"Customer in this chunk: {first_chunk['CustomerID'].nunique()}")

        chunk_to_get = 1
        print(f"Processing chunk number: {chunk_to_get}")
        print("\n")



        if all(col in first_chunk.columns for col in ['StockCode', 'Description', 'InvoiceDate', 'Quantity']):
            print("--- Finished Chunk Data  ---")
            output_df = first_chunk[['StockCode', 'Description', 'InvoiceDate', 'Quantity']]
            print(output_df.head(10))  # Display the head of the extracted columns
        else:
            print("\nWarning: One or more of the required columns ('StockCode', 'Description', 'InvoiceDate', 'Quantity') not found in the CSV file.")

        if 'Quantity' in first_chunk.columns:
            print(f"\nTotal mean of first chunk quantity: {first_chunk['Quantity'].mean():.2f}")
        else:
            print("\nWarning: 'Quantity' column not found in the first chunk.")

        try:
            customer_spending = analyze_customer_purchase_volume(file_path, chunk_size=chunk_size)
            if customer_spending is not None and not customer_spending.empty:


                print("\n--- Top Customers by Total Purchase Value (Across Entire File) ---")
                print(customer_spending.head(10))  # Display the top 10 spending customers
                most_valuable_customer = customer_spending.index[0]
                total_spent = customer_spending.iloc[0]
                print(f"\n--- Customer with Highest Purchase Value ---")



                print(f"Customer ID: {most_valuable_customer}, Total Amount Spent: {total_spent:.2f}")

                top_n = 10
                top_customers = customer_spending.head(top_n)
                plt.figure(figsize=(12, 6))
                sns.barplot(x=top_customers.index.astype(str), y=top_customers.values, palette="viridis")
                plt.xlabel("Customer ID")
                plt.ylabel("Total Purchase Value")
                plt.title(f"Top {top_n} Customers by Purchase Value")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                plt.show()
            else:
                print("\nCould not perform full customer purchase volume analysis or no customer spending data available for plotting.")

        except Exception as e:
            print(f"An error occurred during customer purchase volume analysis or plotting: {e}")

    except FileNotFoundError:
        print(f"Error: CSV file not found at {file_path} in read_csv_file.")
        return None
    except StopIteration:
        # num_lines = 0
        print("Warning: The CSV file is empty or has fewer rows than the chunk size.")
    except KeyError as e:
        print(f"Error: Column '{e}' not found in the CSV file in read_csv_file.")
    except Exception as e:
        print(f"An unexpected error occurred in read_csv_file: {e}")
    return [],0,0


    print(f"\n ==================== [Final RAM USAGE: {psutil.virtual_memory().percent} %] ===========================")


      # for plot graph




#==========================================================================================🌍[end csv read]🌍======================================
#data cleanning
def clean_description(description):
    if isinstance(description, str):
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', description)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()
    return ''
#</>====================================================================================={🌐[start os read]🌐}++++++++++++++++++++++++++++++
def os_read_and_clean_data(file_path, description_column_index=2, quantity_column_index=3, encoding='ISO-8859-1',chunk_size=4096):
    cleaned_description_counts = Counter()
    total_lines_processed = 0
    remaining_bytes = b''  # Initialize remaining as bytes

    # [ start time of os read] ⏰
    start_time = time.time()
    mem_usage = get_memory_usage()
    # =========================⏰

    try:
        with open(file_path, 'rb') as file:
            file_descriptor = file.fileno()
            header_skipped = False
            while True:
                content_bytes = os.read(file_descriptor, chunk_size)
                # content_bytes = file.read()
                if not content_bytes:
                    break

                # file_content = file.read()  # Read the whole file at once

                combined_bytes = remaining_bytes + content_bytes
                decoded_content = combined_bytes.decode(encoding, errors='ignore')
                # lines = content_bytes.splitlines()
                lines = decoded_content.splitlines()
                remaining_bytes = lines[-1].encode() if lines else b'' # Encode remaining back to bytes

 
                for line in lines[:-1]:
                    total_lines_processed += 1
                    if not header_skipped:
                        header_skipped = True
                        continue

                    parts = line.split(',')
                    if len(parts) > max(description_column_index, quantity_column_index):
                        description = parts[description_column_index].strip()
                        cleaned_desc = clean_description(description)

                        if cleaned_desc:
                            try:
                                quantity_str = parts[quantity_column_index].strip()
                                quantity = int(quantity_str)
                                cleaned_description_counts[cleaned_desc] += quantity
                            except (IndexError, ValueError):
                                cleaned_description_counts[cleaned_desc] += 1

            # Process any remaining part of the last line (which is in 'decoded_content')
            if decoded_content.endswith(lines[-1]): # Check if remaining was part of the last decoded chunk
                remaining_final = lines[-1]
                parts = remaining_final.split(',')
                if len(parts) > max(description_column_index, quantity_column_index):
                    description = parts[description_column_index].strip()
                    cleaned_desc = clean_description(description)
                    if cleaned_desc:
                        try:
                            quantity_str = parts[quantity_column_index].strip()
                            quantity = int(quantity_str)
                            cleaned_description_counts[cleaned_desc] += quantity
                        except (IndexError, ValueError):
                            cleaned_description_counts[cleaned_desc] += 1

        # [end time of os read]---⏰------------------------

        end_time = time.time()
        mem_after = get_memory_usage()

        time_taken = end_time - start_time
        memory_used = time_taken - mem_usage
        #-------------------------------⏰----------------

        return total_lines_processed, cleaned_description_counts, time_taken, memory_used


    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return 0, Counter()
    except OSError as e:
        print(f"Error reading file with os.read: {e}")
        return 0, Counter()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0, Counter()
    # return total_lines_processed, cleaned_description_counts
        # return total_lines_processed, cleaned_description_counts, (time_taken, memory_used)


def os_read_and_get_customer_quantity(file_path, customer_id_column_index=6, quantity_column_index=3, encoding='ISO-8859-1', chunk_size=4096):
    """
    Reads a CSV file using os.read and calculates the total quantity bought by each customer.
    """


    customer_quantity_counts = Counter()
    remaining_bytes = b''

    try:
         with open(file_path, 'rb') as f:
            file_descriptor = f.fileno()
            header_skipped = False
            while True:
                content_bytes = os.read(file_descriptor, chunk_size)
                if not content_bytes:
                    break

                combined_bytes = remaining_bytes + content_bytes
                decoded_content = combined_bytes.decode(encoding, errors='ignore')
                lines = decoded_content.splitlines()
                remaining_bytes = lines[-1].encode(encoding) if lines else b''

                for line in lines[:-1]:
                    if not header_skipped:
                        header_skipped = True
                        continue

                    parts = line.split(',')
                    if len(parts) > max(customer_id_column_index, quantity_column_index):
                        customer_id_str = parts[customer_id_column_index].strip()
                        quantity_str = parts[quantity_column_index].strip()

                        if customer_id_str:
                            try:
                                customer_id = int(customer_id_str)
                                quantity = int(quantity_str)
                                customer_quantity_counts[customer_id] += quantity
                            except ValueError:
                                pass

            if remaining_bytes:
                decoded_remaining = remaining_bytes.decode(encoding, errors='ignore')
                lines = decoded_remaining.splitlines()
                for line in lines:
                    parts = line.split(',')
                    if len(parts) > max(customer_id_column_index, quantity_column_index):
                        customer_id_str = parts[customer_id_column_index].strip()
                        quantity_str = parts[quantity_column_index].strip()
                        if customer_id_str:
                            try:
                                customer_id = int(customer_id_str)
                                quantity = int(quantity_str)
                                customer_quantity_counts[customer_id] += quantity
                            except ValueError:
                                pass

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except OSError as e:
        print(f"Error reading file with os.read: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return customer_quantity_counts



#</>==============================================================================================={🌐[end os read]🌐}++++++++++++++++++++++++++++++

# =============================================================================================================== (>🏗️[ start buffered read]🏗️<)===========================-

def buffered_read(file_path, num_lines=1000000):
    # [ start time of os read] ⏰
    start_time = time.time()
    mem_usage = get_memory_usage()
    # =========================⏰
    try:
        with open(file_path, 'r' ,encoding='ISO-8859-1',buffering=16 * 1024) as f:
            lines = [f.readline().strip() for _ in range(num_lines)]

        # return lines
        # [end time of os read]---⏰------------------------
        end_time = time.time()
        time_taken = end_time - start_time
        memory_used = time_taken - mem_usage
        #-------------------------------⏰----------------

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred during buffered read: {e}")
        return []

    # return lines
    return lines, time_taken, memory_used




def clean_description(description):
    if isinstance(description, str):
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', description)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()
    return ''

def calculate_mean_quantity(lines, description_column_index=2, quantity_column_index=3):
        # start_time = time.time()
        # mem_usage = get_memory_usage()
    product_quantities = defaultdict(list)
    total_processed = 0
    for line in lines:
        total_processed += 1
        parts = line.split(',')
        # parts = []
        if len(parts) > max(description_column_index, quantity_column_index):
            description = parts[description_column_index].strip()
            cleaned_desc = clean_description(description)
            quantity_str = parts[quantity_column_index].strip()
            if cleaned_desc and quantity_str.isdigit():
                try:
                    quantity = int(quantity_str)
                    product_quantities[cleaned_desc].append(quantity)
                except ValueError:
                    pass
    product_mean_quantity = {}
    for product, quantities in product_quantities.items():
        if isinstance(quantities, list) and len(quantities) > 0:
            try:
                mean_quantity = sum(quantities) / len(quantities)
                product_mean_quantity[product] = mean_quantity
            except Exception as e:
                print(f"Error calculating mean for {product}: {e}")
                product_mean_quantity[product] = 0.0  # Set to 0 if there's an error
        else:
            product_mean_quantity[product] = 0.0  # Handle empty list
    # product_mean_quantity = {
    #       product: sum(quantities) / len(quantities)
    #       for product, quantities in product_quantities.items() if quantities
    # }
    print(f"Total lines processed for mean calculation: {total_processed}")
    return product_mean_quantity

def plot_mean_quantity(mean_quantity, top_n=10):
    if not mean_quantity:
        print("No product quantity data to plot.")
        return

    sorted_products = sorted(mean_quantity.items(), key=lambda item: item[1], reverse=True)
    top_products = dict(sorted_products[:top_n])

    plt.figure(figsize=(12, 6))
    plt.bar(top_products.keys(), top_products.values(), color='skyblue')
    plt.xlabel("Product Description")
    plt.ylabel("Mean Quantity Bought")
    plt.title(f"Top {top_n} Products by Mean Quantity Bought")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()



# ================================================================================== (>🏗️[end buffered read]🏗️<)=============================================

#====================================================================================== 🛎️[encode read]🛎️ ==============================

# code code read
def encode_read(file_path, num_lines=1000000):
# start time of encode read ========⏰==============================
    start_time = time.time()
    mem_usage = get_memory_usage()
#  =================================⏰=====

    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            lines = [line.strip().encode('utf-8').decode('utf-8') for _, line in zip(range(num_lines), f)]
      # end time of encode read ======⏰===============================
        end_time = time.time()
        time_taken = end_time - start_time
        memory_used = time_taken - mem_usage
      #  ==============================⏰=======
        return lines
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred during encoded read: {e}")
        return []

    return lines, time_taken, memory_used


def clean_description(description):
    if isinstance(description, str):
        cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', description)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()
    return ''

def calculate_product_percentile(lines, product_name="IVORY KNITTED MUG COSY", description_column_index=2, quantity_column_index=3):
    product_quantities = []
    all_product_quantities = defaultdict(list)
    total_processed = 0

    cleaned_target_product = clean_description(product_name)

    for line in lines:
        total_processed += 1

        parts = line.split(',')
        if len(parts) > max(description_column_index, quantity_column_index):
            description = parts[description_column_index].strip()
            cleaned_desc = clean_description(description)
            quantity_str = parts[quantity_column_index].strip()

            if quantity_str.isdigit():
                try:
                    quantity = int(quantity_str)
                    all_product_quantities[cleaned_desc].append(quantity)
                    if cleaned_desc == cleaned_target_product:
                            product_quantities.append(quantity)
                except ValueError:
                    pass

    if product_quantities and all_product_quantities:
      percentiles = np.arange(0, 101, 10)
      percentile_values = np.percentile(product_quantities, percentiles)
      percentile_dict = {f"{p} %": val for p, val in zip(percentiles, percentile_values)}

      print(f"Total lines processed for percentile calculation: {total_processed}")
      print(f"\n--- Percentiles of Quantity for '{product_name}' ---")
      for p, val in percentile_dict.items():
          print(f"{p}: {val}")

      return cleaned_target_product, percentile_dict
    else:
        print(f"No quantity data found for '{product_name}'.")
        return None, None, None

def plot_percentile_values(product_name, percentile_data):
    if not percentile_data:
        print(f"No percentile data available to plot for '{product_name}'.")
        return

    percentiles = list(percentile_data.keys())
    values = list(percentile_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(percentiles, values, color='lightcoral')
    plt.xlabel("Percentile")
    plt.ylabel("Quantity")
    plt.title(f"Percentile Values of Quantity for '{product_name}'")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()





#==================================================================================== 🛎️[encode read]🛎️ ==============================

#=====================================================================================🛫[mmap read]🛫=======================================
def mmap_read(file_path,encoding='ISO-8859-1'):
    # # [=====================start time of mmap read =====⏰====================]
    start_time = time.time()
    mem_usage = get_memory_usage()
    # #=================================⏰===============================

    # Reads a file and returns the lines.  This version uses readlines().
    # Args:
    # file_path (str): The path to the file.
    # Returns: list: A list of strings, where each string is a line from the file.
    # Returns an empty list on error.

    try:
        with open(file_path, 'rb') as f:
            # lines = f.readlines()
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                decoded_data = mm.read().decode(encoding, errors='ignore')
                lines = decoded_data.splitlines()
        # # [=====================end time of mmap read ===⏰======================]
        end_time = time.time()
        time_taken = end_time - start_time
        memory_used = time_taken - mem_usage
        # #==============================================⏰==================
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return lines, time_taken, memory_used


def calculate_monthly_sales(lines):
            # Calculates the total sales for each month from the provided lines.
            # This function assumes that the input 'lines' is a list of strings,
            # where each string represents a row of data, and that the date is
            # in a format that can be parsed to extract the month.
            # Args:lines (list): A list of strings, where each string is a line from the file.

            # Returns:dict: A dictionary where keys are month numbers (1-12) and values are
        #  the total quantities sold in that month.
            #           Returns an empty dict if input data is invalid or empty.

    monthly_sales = defaultdict(int)
    if not lines:
        print("Error: Inputata is empty.")
        return {}

    for line in lines:
        print(f"Line type: {type(line)}, content: {line[:50]}")
        parts = line.strip().split(',')
        if len(parts) >= 4:  #  Check if the line has enough columns
            try:
                invoice_date = parts[2].strip()
                quantity = int(parts[3].strip())

                        # handle different date formats
                if '/' in invoice_date:
                    month = int(invoice_date.split('/')[1])
                elif '-' in invoice_date:
                     month = int(invoice_date.split('-')[1])
                else:
                    print(f"Skipping row with unrecognised date format: {invoice_date}")
                    continue

                if 1 <= month <= 12:
                    monthly_sales[month] += quantity
                else:
                    print(f"Skipping row with invalid month: {month}, date: {invoice_date}")


            except ValueError:
                print(f"Skipping row due to invalid quantity or date: {line}")
            except IndexError:
                print(f"Skipping row due to missing data: {line}")
        else:
            print(f"Skipping row due to insufficient data: {line}")

    return monthly_sales



def get_month_name(month_num):
            # Converts a month number (1-12) to its name.
            # Args:month_num (int): The month number (1 for January, 12 for December).
            # Returns:str: The name of the month, or "Invalid Month" if the number is not valid.

    if not isinstance(month_num, int):
        return "Invalid Month"
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    return month_names.get(month_num, "Invalid Month")
def display_best_selling_month(monthly_sales):
            # Displays the best selling month and the details of monthly sales.
            # Args: monthly_sales (dict): A dictionary where keys are month numbers (1-12)and values are the total quantities sold in that month.

    if not monthly_sales:
        print("No monthly sales data to display.")
        return

    best_selling_month = max(monthly_sales, key=monthly_sales.get)
    best_selling_month_name = get_month_name(best_selling_month)
    quantity = monthly_sales[best_selling_month]

    print("\n--- Best Selling Month ---")
    print(f"Month: {best_selling_month_name} ({best_selling_month}), Total Quantity Sold: {quantity}")

    print("\n--- Monthly Sales Details ---")
    for month_num, total_quantity in sorted(monthly_sales.items()):
        month_name = get_month_name(month_num)
        print(f"{month_name}: {total_quantity} units")

def plot_monthly_sales(monthly_sales):
            # Plots a bar graph of monthly sales.
            # Args:monthly_sales (dict): A dictionary where keys are month numbers (1-12)and values are the total quantities sold in that month.

    if not monthly_sales:
        print("No monthly sales data to plot.")
        return

    months = list(monthly_sales.keys())
    quantities = list(monthly_sales.values())
    month_names = [get_month_name(month) for month in months]

    plt.figure(figsize=(10, 6))
    plt.bar(month_names, quantities, color='skyblue')
    plt.xlabel("Month")
    plt.ylabel("Total Quantity Sold")
    plt.title("Monthly Sales")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()



#=========================================================================================🛫[mmap read]🛫============================

def plot_customer_quantity(customer_quantity, top_n=10, title="Customer Quantity Distribution"):

    if not customer_quantity:
      print("No data available for plotting.")
    return

    sorted_customers = sorted(customer_quantity.items(), key=lambda item: item[1])
    top_customers = dict(sorted_customers[-top_n:])
    bottom_customers = dict(sorted_customers[:top_n])

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.bar(bottom_customers.keys(), bottom_customers.values(), color='red')
    plt.xlabel("Customer ID")
    plt.ylabel("Total Quantity")
    plt.title(f"Bottom {top_n} Customers (Least Quantity)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.subplot(1, 2, 2)
    plt.bar(top_customers.keys(), top_customers.values(), color='green')
    plt.xlabel("Customer ID")
    plt.ylabel("Total Quantity")
    plt.title(f"Top {top_n} Customers (Most Quantity)")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.suptitle(title)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# =======================================================================================<(comparison zone)>======================

def get_memory_usage():
    """Gets the current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # Convert to MB

def compare_reading_methods(file_path):
    results = []


    for func in [read_csv, os_read_and_clean_data, buffered_read, encode_read, mmap_read]:
        func_name = func.__name__

        try:

            # Record memory and time before
            mem_before = get_memory_usage()
            time_start = time.perf_counter()

            lines = func(file_path)



            time_end = time.perf_counter()
            mem_after = get_memory_usage()




            time_taken = time_end - time_start
            memory_used = mem_after - mem_before

            memory_used = max(0, mem_after - mem_before)
            if lines is not None:
                results.append({
                    'Method': func_name,
                    'Time (s)': time_taken,
                    'Memory (MB)': memory_used,
                    'Lines': lines
                })
        except Exception as e:
            print(f"Error in {func_name}: {e}")
            results.append({
                'Method': func_name,
                'Time (s)': 0,
                'Memory (MB)': 0,
                'Lines': []
            })

    # Print results in a formatted table
    print("\nComparison of File Reading Methods:")
    print("-" * 60)
    print("{:<25} | {:<10} | {:<12}".format("Method", "Time (s)", "Memory (MB)"))
    print("-" * 60)
    for result in results:
        print("{:<25} | {:<10.4f} | {:<12.2f}".format(
            result['Method'], result['Time (s)'], result['Memory (MB)']
        ))
    print("-" * 60)

    return results

# =======================================================================================<(comparison zone)>======================


#                                                                        [output zone]




file_path = '/content/drive/MyDrive/data.csv'


# =================================================================================(🎖️[1] read csv file) 🎖️===============================
# ===================================[To find who customer is the best sellers]===============================

#                             Just uncomment code below ================================>>

# top_n = 5
# customer_spending = 0

# lines ,_,_= read_csv(file_path)

# customer_spending = analyze_customer_purchase_volume(file_path)
#                                Stop comment here ===============================>>>>>
# 😀 pass
# =================================================================================(🎖️[1]read csv file)🎖️ ===================================

#><><><><><><><><<<<<<<<<<<<<<<<<<<<<(NEXT)><><<><><><><>>><><><><><><><

#================================================================================== <[✨[2] read os file]✨> =======================================>
# ///////////////////////////////////////[To customer buy least quantity]////////////////////////////
#                             Just uncomment code below ================================>>



# customer_id_column = 6  # Adjust to the correct index of CustomerID
# quantity_column = 3     # Adjust to the correct index of Quantity

# description_column = 2  # Adjust to the correct index
# quantity_column_desc = 3  # Adjust to the correct index

# total_lines, cleaned_counts, time_taken, mem_used = os_read_and_clean_data(
#     file_path,
#     description_column_index=2,
#     quantity_column_index=3,
#     encoding='utf-8',
#     chunk_size=8192
# )

# if cleaned_counts:
#     print(f"Total lines processed (excluding header): {total_lines}")
#     print("\n--- Top 20 Cleaned Product Descriptions by Quantity ---")
#     for desc, count in cleaned_counts.most_common(20):
#         print(f"- {desc}: {count} Items")
# else:
#     print("No cleaned product descriptions found or an error occurred.")

# print("\n")
# customer_quantity_data = os_read_and_get_customer_quantity(file_path, customer_id_column, quantity_column)

# print("\n--- Customer Who Bought the Least Total Quantity (Positive Quantity) ---")
# if customer_quantity_data:
#     plot_customer_quantity(customer_quantity_data, top_n=10, title="Customer Quantity Analysis")

#     # Calculate and print the customer who bought the least (positive quantity)
#     positive_quantity_customers = {cust_id: qty for cust_id, qty in customer_quantity_data.items() if qty > 0}
#     if positive_quantity_customers:
#         least_quantity_customer = min(positive_quantity_customers, key=positive_quantity_customers.get)
#         least_quantity = positive_quantity_customers[least_quantity_customer]
#         print(f"Customer ID: {least_quantity_customer}, Total Quantity Bought: {least_quantity}")
#     else:
#         print("\nNo customers with positive purchase quantities found.")
# else:
#     print("Could not retrieve customer quantity data for analysis.")


#                                Stop comment here ===============================>>>>>
# 😀 pass
#================================================================================= <[✨[2] read os file]✨> =======================================>


#><><><><><><><><<<<<<<<<<<<<<<<<<<<<(NEXT)><><<><><><><>>><><><><><><><

#================================================================================== <[🎊[3] buffered read method]🎊> =================================
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<[mean quantity]>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                             Just uncomment code below ================================>>

# num_lines = 1000
# lines ,_,_ = buffered_read(file_path,num_lines)
# if lines:
#   mean_quantity = calculate_mean_quantity(lines)
#   if mean_quantity:
#     print("\n--- Mean Quantity Bought per Product (Top Products) ---")
#     sorted_mean_quantity = sorted(mean_quantity.items(), key=lambda item: item[1], reverse=True)
#     for product, mean_qty in sorted_mean_quantity[:10]:
#       print(f"- {product} : {mean_qty:.2f} % ")
#     plot_mean_quantity(mean_quantity)
#   else:
#     print("Could not calculate mean product quantity.")
# else:
#   print("NO lines were read from the file.")

#                                Stop comment here ===============================>>>>>
# 😀 pass
#==================================================================================== <[🎊[3] buffered read method]🎊> =================================

#><><><><><><><><<<<<<<<<<<<<<<<<<<<<(NEXT)><><<><><><><>>><><><><><><><
#===================================================================================== <[🎁[4] encode_read]🎁> ================================
# ================================[How much percentile of the product "IVORY KNITTED MUG COSY "]===============================
#                             Just uncomment code below ================================>>
# num_lines = 10000
# product_to_analyze = "IVORY KNITTED MUG COSY "
# lines = encode_read(file_path, num_lines)

# if lines:
#     target_product, percentile_data = calculate_product_percentile(lines, product_to_analyze)
#     if target_product:
#         plot_percentile_values(target_product, percentile_data)
#     else:
#         print(f"Could not calculate percentile for '{product_to_analyze}'.")
# else:
#     print("No lines were read from the file.")
#                                Stop comment here ===============================>>>>>
# 😀 pass
#=================================================================================== <[🎁[4] encode_read]🎁> ================================
#><><><><><><><><<<<<<<<<<<<<<<<<<<<<(NEXT)><><<><><><><>>><><><><><><><
# ==================================================================================] [🏉[5] mmap read]🏉 [=================================
# =========================================================================[which month is the best selling in a year]=======================
#                             Just uncomment code below ================================>>


# lines ,_,_= mmap_read(file_path)
# if lines:
#   monthly_sales = calculate_monthly_sales(lines)
#   display_best_selling_month(monthly_sales)
#   plot_monthly_sales(monthly_sales)
# else:
#   print("No data processed.")
                              #  Stop comment here ===============================>>>>>
# 😀 pass
# =======================================================================================] [🏉[5] mmap read]🏉 [=================================

# ======================================================================================🔆<(comparison zone)🔆>======================
# file_path = '/content/drive/MyDrive/data.csv'  # Replace with your file path

#                             Just uncomment code below ================================>>

# results = compare_reading_methods(file_path)


# if results:
#     fastest_method = min(results, key=lambda x: x['Time (s)'])
#     print(f"\nFastest method: ✨🎉👑 [{fastest_method['Method']} with time: {fastest_method['Time (s)']:.4f} seconds] 👑 🎉✨")

#                                Stop comment here ===============================>>>>>
# =======================================================================================🔆<(comparison zone)>🔆======================

