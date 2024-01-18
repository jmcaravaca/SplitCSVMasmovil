import duckdb
import os
import shutil
import uuid
from loguru import logger
from datetime import datetime


def split_by_grupo(input_file: str, environment: str) -> str:
# Input file name
    if input_file is None:
        raise ValueError("invalid argument")
    # Clear the output folder if it exists
    nfs_drive_folder =  os.path.join("var/nfsharefile", environment)
    output_folder = os.path.join(nfs_drive_folder, "apidata", f"output_{str(uuid.uuid4())}")
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        logger.info("Cleaned Output Folder")
    # Recreate the output folder
    os.makedirs(output_folder)
    logger.info("Created output folder")
    # Create a connection to DuckDB
    con = duckdb.connect()
    try:
        results = {}
        # Read the distinct values directly from the DuckDB database
        distinct_values_query = con.execute(f"SELECT [GRUPO] FROM '{input_file}' GROUP BY [GRUPO]")
        distinct_values = [row[0][0] for row in distinct_values_query.fetchall()]
        logger.debug(distinct_values)
        # Function to execute EXPORT command for each value

        # Iterate over distinct values and create CSV files
        for value in distinct_values:
            logger.info(f"Creating output for {input_file} on value {value}")
            timestamp = datetime.now().isoformat().replace(':', '_')
            outputfile = os.path.join(output_folder, f'output_{value}_{timestamp}.csv')
            query = f"""COPY (SELECT * FROM '{input_file}'
                        WHERE GRUPO = '{value}')
                        TO '{outputfile}' (HEADER, DELIMITER '|');"""
            con.execute(query)
            logger.info(f"Written CSV to {outputfile}")
            results[value] = outputfile.replace(nfs_drive_folder, "X:").replace("/", "\\")
    except Exception as e:
        logger.error(e)
    finally:
        # Close the DuckDB connection
        con.close()
        #shutil.rmtree(output_folder)
        return results

if __name__ == "__main__":
    results = split_by_grupo("csvexample.csv.gz")
    print(results)