import requests
import pandas as pd

while True:

    name = input("Venue Name => ")
    if name == "/":
        break

    address = input("VENUE Address => ")

    params = {
        'api_key_private': 'pri_5c898cc1c63040f0829804b093a988a6',
        'venue_name': name,
        'venue_address': address
    }

    response = requests.request("POST", "https://besttime.app/api/v1/forecasts" , params=params)
    json = response.json()

    if (json['status'] == "OK"):
        print(json['status'])

        df = pd.DataFrame()
        day = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

        analysis = json['analysis']

        for i in range (0,7):
            daydata = analysis[i]['hour_analysis']
            busyness = analysis[i]['day_raw']
            
            dictionary = {'Airport':[] ,'Day':[],'Hour':[], 'Intensity Level':[],'Intensity Status':[], 'Busyness':[]}
            
            for j in range (0,24):
                dictionary['Airport'].append(name)
                dictionary['Day'].append(day[i])
                dictionary['Hour'].append(daydata[j]['hour']) 
                dictionary['Intensity Status'].append(daydata[j]['intensity_txt'])
                dictionary['Intensity Level'].append(daydata[j]['intensity_nr'])
                dictionary['Busyness'].append(busyness[j])

            data = pd.DataFrame(dictionary)
            data = data.sort_values('Hour')
            df = pd.concat([df,data])

        df = df.reset_index(drop= True)
        df.to_csv((name+'.csv'),index=False)
        
    else:
        print("ERROR")
