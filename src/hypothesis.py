def bigquery_compute_cost(init_GB: int, date: str) -> float:
    cost_GB = init_GB - 1000
    if cost_GB > 0 and (date.split("-")[-1] != "01"):
        return cost_GB * (6.25 / 1024)
    else:
        return 0

def snowflake_compute_cost(init_GB : int, date : str = 0) -> float : 
    if init_GB <= 200:  # Less than or equal to 200 GB
        return 2 * (15/60)
    elif init_GB <= 1024:  # Less than or equal to 1 TB (1024 GB)
        return 4 * (15/60)
    elif init_GB <= 2048:  # Less than or equal to 2 TB (2048 GB)
        return 8 * (15/60)
    elif init_GB <= 4096:  # Less than or equal to 4 TB (4096 GB)
        return 16 * (15/60)
    elif init_GB <= 8192:  # Less than or equal to 8 TB (8192 GB)
        return 32 * (15/60)
    elif init_GB <= 16384:  # Less than or equal to 16 TB (16384 GB)
        return 64 * (15/60)
    elif init_GB <= 32768:  # Less than or equal to 32 TB (32768 GB)
        return 128 * (15/60)
    else:
        return -1

def bigquery_storage_cost(init_GB : int) -> float : 
    cost_GB = init_GB - 10
    return cost_GB*0.02 * (cost_GB >= 0)

def snowflake_storage_cost(init_GB : int) -> float : 
    return init_GB*0.04

def DW_hypothesis(choice) : 
    hypothesis = {
        "GB_events" : 600000, 
        "GB_cost" : 0.05
    }

    if choice == "BigQuery" : 

        hypothesis["compute_cost"] = bigquery_compute_cost
        hypothesis["storage_cost"] = bigquery_storage_cost
        hypothesis_label = {
        "Num of events in GB" : " 1GB = 600 000",
        "Ingestion cost" : "0.05$ per GB",
        "Storage cost" : f'10GB Free + {0.02}$ per GB',
        "Compute cost" : f'1TB Free + {6.25}$ per TB',
        "Compute usage" : "Let's assume the compute usage and storage are even in term of GB"
        }



    elif choice == "Snowflake" : 

        compute_cost_label = """
        gross estimation according to the warehouse cluster : \n
            < 200GB/h : 2$/h, \n
            < 1 TB/h : 4$/h,\n
            < 2 TB/h : 8$/h, \n
            < 4 TB/h : 16$/h, \n
            < 8 TB/h : 32$/h, \n
            < 16 TB/h : 64$/h, \n
            < 32 TB/h : 128$/h
        """

        hypothesis_label = {
        "Num of events in GB" : " 1GB = 600 000",
        "Ingestion cost" : "0.05$ per GB",
        "Storage cost" : f'{0.04}$ per GB',
        "Compute cost" : f'Assuming compute will last 15min max : {compute_cost_label}',
        "Compute usage" : "Let's assume the compute usage and storage are even in term of GB"
        }

        hypothesis["compute_cost"] = snowflake_compute_cost
        hypothesis["storage_cost"] = snowflake_storage_cost

    return [hypothesis, hypothesis_label]
