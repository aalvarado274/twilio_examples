import os, csv
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

# You can also type the Account SID and Auth Token directly, instead of using an environment variable.
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
print('Getting all subaccounts...')
client = Client(account_sid, auth_token)

#This gets the list of all subaccounts
accounts = client.api.v2010.accounts.list()
account_sids_dict = {}
for record in accounts:
    account_sids_dict[record.sid] = record.friendly_name

print('Report creation started. Please wait...')
with open('Subaccounts usage.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    header = ['Subaccount name', 'Account SID', 'Usage by subaccount']    
    writer.writerow(header)
    for i in account_sids_dict.keys():
        try:
            client = Client(account_sid, auth_token, i)

            # Use this if you want to get any month's usage.
            # records = client.usage.records.list(start_date = "2022-03-01", end_date="2022-03-31")

            # Use this if you want to get last month's usage only.
            records = client.usage.records.last_month.list()

            total = 0
            for record in records:
                # print(record.start_date, record.end_date, record.category, record.count,
                # record.count_unit, record.price, record.price_unit)
                total += record.price
            # print(i, '\t', '$', total)
            data = [account_sids_dict[i], i, '$'+str(total)]
            writer.writerow(data)
        except:
            print(f'Subaccount {i} did not exist in this month')
            data = [account_sids_dict[i], i, '$0.00','Subaccount did not exist in this month.']
            writer.writerow(data)
print("Report created succesfully!")