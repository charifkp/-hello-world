from os.path import join
import timeit
import time
from functools import partial
import psutil, os
import gc
import csv
import matplotlib.pyplot as plt

# -----------------------
# Check your memory before starting.
print(f"Initial RAM usage: {psutil.virtual_memory().percent}%")
print("-----------------------------------")

# File path
file_path = '/content/drive/MyDrive/data.csv'  # Adjust as needed


# -----------------------
# Define the reading methods

def buffered_read(file_path, num_lines=1000):
    with open(file_path, 'r',buffering=16*1024, encoding='ISO-8859-1') as f:
        lines = [f.readline().strip() for _ in range(num_lines)]
    return lines

def os_read(file_path, num_lines=1000):
    try:
        # Open the file using os.open and get a file descriptor
        fd = os.open(file_path, os.O_RDONLY)

        try:
            # Read 4KB chunks from the file using the file descriptor
            content = os.read(fd, 4096)  # Read 4KB at a time
            # Decode the bytes and split into lines
            lines = content.decode('ISO-8859-1').splitlines()[:num_lines]

        except Exception as e:
            # Catch any error during the read and decoding process
            print(f"Error reading the file: {e}")
            lines = []

        finally:
            # Always close the file descriptor when done
            os.close(fd)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        lines = []

    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        lines = []

    return lines

def encode_read(file_path, num_lines=1000):
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        lines = [line.strip().encode('utf-8').decode('utf-8') for _, line in zip(range(num_lines), f)]
    return lines

# -----------------------
# Existing CSV display functions
def display_csv_beautifully(file_path, num_rows=10):
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        header = f.readline().strip().split(',')
        rows = [line.strip().split(',') for _, line in zip(range(num_rows), f)]
    columns = list(zip(*([header] + rows)))
    col_widths = [max(len(str(item)) for item in col) + 2 for col in columns]  # +2 for padding

    # Display header
    header_line = " | ".join([h.ljust(w) for h, w in zip(header, col_widths)])
    print(header_line)
    print("-" * len(header_line))

    d_formatrow_1 = []
    # Display rows
    for row in rows:
        formatted_row = " --> ".join([val.ljust(w) for val, w in zip(row, col_widths)])
        print(formatted_row)
        d_formatrow_1.append(formatted_row)
    return d_formatrow_1

def display_selected_columns_by_invoice(file_path, invoice_no='C581228'):
    selected_indices = [0, 4, 5]  # InvoiceNo, StockCode, Description
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        full_header = f.readline().strip().split(',')
        header = [full_header[i] for i in selected_indices]
        rows = []

        for line in f:
            full_row = line.strip().split(',')
            if full_row[0] == invoice_no:
                rows.append([full_row[i] for i in selected_indices])

    if not rows:
        print(f"No data found for InvoiceNo: {invoice_no}")
        return

    max_width = 25
    columns = list(zip(*([header] + rows)))
    col_widths = [min(max(len(str(i)) for i in col) + 6, max_width) for col in columns]

    header_line = " | ".join([str(h)[:w].ljust(w) for h, w in zip(header, col_widths)])
    print(header_line)
    print("-" * len(header_line))

    d_formatrow_2 = []
    for row in rows:
        formatted_row = " --> ".join([str(val)[:w].ljust(w) for val, w in zip(row, col_widths)])
        print(formatted_row)
        d_formatrow_2.append(formatted_row)
    return d_formatrow_2

def pretty_print_csv(file_path, num_rows=5):
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as f:
            header = f.readline().strip().split(',')
            all_rows = [line.strip().split(',') for line in f]

        last_rows = all_rows[-num_rows:]
        if not last_rows:
            print("CSV file is empty or has fewer rows than requested.")
            return

        columns = list(zip(*([header] + last_rows)))
        col_widths = [max(len(str(item)) for item in col) + 1 for col in columns]

        header_line = " | ".join([h.ljust(w) for h, w in zip(header, col_widths)])
        print(header_line)
        print("-" * len(header_line))

        d_formatrow_3 = []
        for row in last_rows:
            formatted_row = " --> ".join([val.ljust(w) for val, w in zip(row, col_widths)])
            print(formatted_row)
            d_formatrow_3.append(formatted_row)
        return d_formatrow_3

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# -----------------------
 

# Get current memory usage
def get_memory_usage_mb():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # in MB

# Measure execution time + memory usage
def measure_memory(func, *args, **kwargs):
    gc.collect()  # Clean up before measuring
    mem_before = get_memory_usage_mb()

    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    gc.collect()  # Clean again after
    mem_after = get_memory_usage_mb()

    mem_used = mem_after - mem_before
    time_taken = (end - start) * 1000  # in milliseconds

    return result, time_taken, mem_used
 
# -----------------------


def get_first_invoice_no(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            return row['InvoiceNo']  # get first InvoiceNo found in file
# Comparison and testing function

def run_comparison(file_path='/content/drive/MyDrive/data.csv'):
    # print("Starting Comparison...\n")
    # sample_test()
    # Define partial functions for display_selected_columns_by_invoice and pretty_print_csv
    display_selected = partial(display_selected_columns_by_invoice, file_path)
    pretty_print = partial(pretty_print_csv, file_path, num_rows=10)

    # print("Buffered Read Comparison")
    # print("=" * 80)
    buffered_result, buffered_time, buffered_memory = measure_memory(buffered_read, file_path, num_lines=10000000)
    # print(f"Buffered Read - Time: {buffered_time:.2f} ms, Memory: {buffered_memory / 1024:.2f} MB")
    # print("=" * 80)

    # print("OS Read Comparison")
    # print("=" * 80)
    os_result, os_time, os_memory = measure_memory(os_read, file_path, num_lines=1000000)
    # print(f"OS Read - Time: {os_time:.2f} ms, Memory: {os_memory / 1024:.2f} MB")
    # print("=" * 80)

    # print("Encode Read Comparison")
    # print("=" * 80)
    encode_result, encode_time, encode_memory = measure_memory(encode_read, file_path, num_lines=10000000)
    # print(f"Encode Read - Time: {encode_time:.2f} ms, Memory: {encode_memory / 1024:.2f} MB")
    # print("=" * 80)

    # Measure execution time for existing functions
    display_beautiful_time = timeit.timeit(lambda: display_csv_beautifully(file_path, num_rows=10), number=1) * 1000 / 10
    print("-" * 70)

    display_selected_time = timeit.timeit(display_selected, number=1) * 1000 / 10
    print("-" * 70)

    pretty_print_time = timeit.timeit(pretty_print, number=1) * 1000 / 10
    print("-" * 70)

    # Print comparison results for existing and new methods
    print("\n")
    print("-" * 70)
    print(f"{'Function':<40} | {'Read_Time (ms)'} | {'Memory (MB)'} |")
    print("-" * 70)
    # print(f"{'display_csv_beautifully':<40} | {display_beautiful_time:10.2f} | {'--':<10}")
    # print(f"{'display_selected_columns_by_invoice':<40} | {display_selected_time:10.2f} | {'--':<10}")
    # print(f"{'pretty_print_csv':<40} | {pretty_print_time:10.2f} | {'--':<10}")


    print(f"{'Buffered Read':<40} | {buffered_time:10.2f} | {buffered_memory / 1024:10.2f}")
    print(f"{'OS Read':<40} | {os_time:10.2f} | {os_memory / 1024:10.2f}")
    print(f"{'Encode Read':<40} | {encode_time:10.2f} | {encode_memory / 1024:10.2f}")
    print("-" * 55)

    # Visual comparison
    read_times = [buffered_time, os_time, encode_time]
    memory_usages = [buffered_memory / 1024, os_memory / 1024, encode_memory / 1024]
    labels = ['Buffered Read', 'OS Read', 'Encode Read']
    plot_comparison_graph(read_times, memory_usages, labels)

def plot_comparison_graph(read_times, memory_usages, labels):
    x = range(len(labels))

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Read Time
    color = 'tab:blue'
    ax1.set_xlabel('Read Method')
    ax1.set_ylabel('Read Time (ms)', color=color)
    bars1 = ax1.bar([i - 0.2 for i in x], read_times, width=0.4, label='Read Time (ms)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)

    # Plot Memory Usage on second y-axis
    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Memory Usage (MB)', color=color)
    bars2 = ax2.bar([i + 0.2 for i in x], memory_usages, width=0.4, label='Memory (MB)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Comparison of Read Methods: Time vs Memory')
    plt.tight_layout()
    plt.show()


    




# Run the comparison
   # You can change this dynamically
run_comparison()

 
print("< 🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉🙉>")
print("💽<<<=================================================>>>🔽")

# -----------------------
# Clean up and print final memory usage
gc.collect()
print(f"Final RAM usage: {psutil.virtual_memory().percent}%")

