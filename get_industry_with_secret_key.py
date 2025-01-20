import psycopg2
import csv

DB_HOST = '192.168.1.69'
DB_NAME = 'mppcb_esc_test'
DB_USER = 'admin'
DB_PASSWORD = 'admin'

def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()

        query = """
        SELECT industry.mppcb_id, count(industry.mppcb_id) "count", industry.secret_key, ambient.Id
        FROM public."Industry_Data_industrydetails" industry
        JOIN public."Industry_Data_ambientdetails" ambient
        ON industry.mppcb_id=ambient.industry_id
        JOIN public."Industry_Data_analyzersensordetails" sensor
        ON ambient.id=sensor.ambient_id
        JOIN public."Industry_Data_parameterrealtimedata" param
        ON sensor.id=param.analyzer_id
        GROUP BY industry.mppcb_id, ambient.Id
        HAVING COUNT(industry.mppcb_id) % 7 = 0 
        AND industry.secret_key IS NOT NULL
        ORDER BY industry.mppcb_id DESC
        """
        
        cursor.execute(query)

        rows = cursor.fetchall()

        output_file = "esc_ids.csv"
        
        # Open the CSV file to write the data
        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["mppcb_id", "count", "password", "secret_key", "ambient_id"])
            
            for row in rows:
                writer.writerow([row[0], row[1], "Mppcb@123", row[2], row[3]])

        print(f"Data successfully exported to {output_file}")
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error while connecting to PostgreSQL: {e}")

if __name__ == '__main__':
    connect_to_db()