import psycopg2
import psycopg2.extras
from config import config

def copy_from_csv(conn, cursor, table_name, csv_file_path):
    #Open the csv file
    with open(r'C:\Users\syedk\Documents\investigation_project_v3\homicide_media_data.csv', 'r', encoding='ISO-8859-1') as file:
        #copy data from the csv file to the table
        cursor.execute('SET datestyle = "ISO, DMY";')
        cursor.copy_expert("""COPY homicide_v1 (news_report_URL,
                            news_report_platform,
                            date_of_publication ,
                            author,
                            news_report_headline,
                            wire_service ,
                            no_of_subscribers,
                            victim_name ,
                            date_of_death,
                            age_of_victim ,
                            race_of_victim,
                            type_of_location ,
                            place_of_death_town,
                            place_of_death_province ,
                            sexual_assault ,
                            mode_of_death_specific ,
                            mode_of_death_general, 
                            robbery,
                            suspect_arrested ,
                            suspect_convicted,
                            perpetrator_name ,
                            perpetrator_relationship_to_victim ,
                            multiple_murder,
                            intimate_femicide,
                            extreme_violence,
                            notes)
        FROM STDIN WITH CSV HEADER DELIMITER ','
        """, file)
        print(f"Data copied successfully to homicide_v1.")

def connect():
    connection = None
    csr = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database ...')
        connection = psycopg2.connect(**params)
        csr = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        csr.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        # Drop the table if it already exists
        
        csr.execute("DROP TABLE IF EXISTS homicide_v1 CASCADE")
        
        create_script_homicide = '''CREATE TABLE homicide_v1 (
                            article_id SERIAL PRIMARY KEY,
                            news_report_id UUID DEFAULT uuid_generate_v4(), 
                            news_report_url VARCHAR(255) ,
                            news_report_platform VARCHAR(255),
                            date_of_publication DATE,
                            author VARCHAR(255),
                            news_report_headline VARCHAR(255),
                            wire_service VARCHAR(255),
                            no_of_subscribers INT,
                            victim_name VARCHAR(255),
                            date_of_death DATE,
                            age_of_victim INT,
                            race_of_victim VARCHAR(255),
                            type_of_location VARCHAR(255),
                            place_of_death_town VARCHAR(255),
                            place_of_death_province VARCHAR(100),
                            sexual_assault VARCHAR(255),
                            mode_of_death_specific VARCHAR(100),
                            mode_of_death_general VARCHAR(255),
                            robbery VARCHAR(10), 
                            suspect_arrested VARCHAR(255),
                            suspect_convicted VARCHAR(255),
                            perpetrator_name VARCHAR(255),
                            perpetrator_relationship_to_victim VARCHAR(255),
                            multiple_murder BOOLEAN,
                            intimate_femicide VARCHAR(10),
                            extreme_violence VARCHAR(10),
                            notes VARCHAR(255)
                            )'''                   
        csr.execute(create_script_homicide)
        print("homicide_news Table created successfully in public")
        copy_from_csv(connection, csr, 'homicide_v1', r'C:\Users\syedk\Documents\investigation_project_v3\homicide_media_data.csv')
        
        
        connection.commit()

        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if csr is not None:
            csr.close()
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
            
if __name__ == "__main__":
    connect()
