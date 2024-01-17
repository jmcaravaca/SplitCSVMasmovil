import duckdb
import os
import shutil
from loguru import logger


# Input file name
input_file = 'csvexample.csv.gz'

# Clear the output folder if it exists
output_folder = 'output'
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
    logger.info("Cleaned Output Folder")
# Recreate the output folder
os.makedirs(output_folder)
logger.info("Created output folder")
# Create a connection to DuckDB
con = duckdb.connect()

# Read the distinct values directly from the DuckDB database
distinct_values_query = con.execute(f"SELECT [GRUPO] FROM '{input_file}' GROUP BY [GRUPO]")
distinct_values = [row[0][0] for row in distinct_values_query.fetchall()]
logger.debug(distinct_values)
# Function to execute EXPORT command for each value
def export_to_csv(grupo_value):
    query = f"COPY (SELECT * FROM '{input_file}' WHERE GRUPO = '{grupo_value}') TO '{os.path.join(output_folder, f'output_{grupo_value}.csv')}' (HEADER, DELIMITER '|');"
    con.execute(query)

# Iterate over distinct values and create CSV files
for value in distinct_values:
    logger.debug(f"Creating output for {input_file} on value {value}")
    export_to_csv(value)

# Close the DuckDB connection
con.close()
