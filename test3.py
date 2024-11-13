import pandas as pd
from datetime import datetime
master_data ={
    "Aadil 2024-09": {
        "lease_details": [
            {
                "_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "formation": "Arbuckle, LKC",
                "lease_number": "",
                "name": "Aadil"
            }
        ],
        "well_details": [
            {
                "_id": "d1dfd15c-196b-415f-846c-7bd458459bfe",
                "api_number": "15-009-25987",
                "lease": "Aadil",
                "name": "Aadil 1-19",
                "well_status": "Shut-in",
                "well_type": "OIL"
            }
        ],
        "well_days_on": [
            {
                "facility_name": "Aadil",
                "days_on": 30.0,
                "Date": "2024-09"
            }
        ],
        "prod_data": [
            {
                "facility_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "production_stream": "oil",
                "qualifier": "custody_transferred",
                "record_date": 1725148800,
                "facility_name": "Aadil",
                "facility_type": "lease",
                "volume": "110.22",
                "Date": "2024-09"
            },
            {
                "facility_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "production_stream": "oil",
                "qualifier": "measured",
                "record_date": 1725148800,
                "facility_name": "Aadil",
                "facility_type": "lease",
                "volume": "160.32",
                "Date": "2024-09"
            }
        ],
        "facility_measurement_data": []
    },
    "Aadil 2024-10": {
        "lease_details": [
            {
                "_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "formation": "Arbuckle, LKC",
                "lease_number": "",
                "name": "Aadil"
            }
        ],
        "well_details": [
            {
                "_id": "d1dfd15c-196b-415f-846c-7bd458459bfe",
                "api_number": "15-009-25987",
                "lease": "Aadil",
                "name": "Aadil 1-19",
                "well_status": "Shut-in",
                "well_type": "OIL"
            }
        ],
        "well_days_on": [
            {
                "facility_name": "Aadil",
                "days_on": 24.0,
                "Date": "2024-10"
            }
        ],
        "prod_data": [
            {
                "facility_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "production_stream": "oil",
                "qualifier": "custody_transferred",
                "record_date": 1727740800,
                "facility_name": "Aadil",
                "facility_type": "lease",
                "volume": "302.27",
                "Date": "2024-10"
            },
            {
                "facility_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "production_stream": "oil",
                "qualifier": "measured",
                "record_date": 1727740800,
                "facility_name": "Aadil",
                "facility_type": "lease",
                "volume": "432.53",
                "Date": "2024-10"
            }
        ],
        "facility_measurement_data": []
    },
    "Aadil 2024-08": {
        "lease_details": [
            {
                "_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "formation": "Arbuckle, LKC",
                "lease_number": "",
                "name": "Aadil"
            }
        ],
        "well_details": [
            {
                "_id": "d1dfd15c-196b-415f-846c-7bd458459bfe",
                "api_number": "15-009-25987",
                "lease": "Aadil",
                "name": "Aadil 1-19",
                "well_status": "Shut-in",
                "well_type": "OIL"
            }
        ],
        "well_days_on": [
            {
                "facility_name": "Aadil",
                "days_on": 31.0,
                "Date": "2024-08"
            }
        ],
        "prod_data": [
            {
                "facility_id": "465fac7a-087c-411b-acf9-16d332ea380e",
                "production_stream": "oil",
                "qualifier": "measured",
                "record_date": 1722470400,
                "facility_name": "Aadil",
                "facility_type": "lease",
                "volume": "-125.8",
                "Date": "2024-08"
            }
        ],
        "facility_measurement_data": []
    }
}
table_data_list=[]
for key, value in master_data.items():
    table_data_dict ={}
    table_data_dict['Period'] =datetime.strptime(key.split(' ')[1], "%Y-%m").strftime("%m/%Y") 
    table_data_dict['LSE Code'] = "LSECODE"
    table_data_dict['Lease'] = master_data[key]['lease_details'][0]['lease_number']
    table_data_dict['Lease Name']=key.split(' ')[0]
    table_data_dict['Formation']=master_data[key]['lease_details'][0]['formation']
    well_details = master_data[key]['well_details']
    well_days_on =master_data[key]['well_days_on']
    table_data_dict['SI Oil Wells'] = sum(1 for well in well_details if well['well_status'] == "Shut-In" and well['well_type']=="OIL")
    table_data_dict['PR Oil Wells'] = sum(1 for well in well_details if well['well_status'] == "Active" and well['well_type']=="OIL")
    table_data_dict['Total Prod Days'] = sum([float(well['days_on']) for well in well_days_on])
    prod_data = master_data[key]['prod_data']
    print("PERD",prod_data)
    current_date = list(filter(lambda x:x['production_stream'] =="oil" and x['qualifier']=="measured",prod_data))
    date = current_date[0]['record_date'] if current_date else None
    print("CURRENT",date)
    table_data_list.append(table_data_dict)

df=pd.DataFrame(table_data_list)
df.sort_values(by=['Period'],inplace=True)
print(df)

   
