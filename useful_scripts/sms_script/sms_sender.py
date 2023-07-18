from twilio.rest import Client

account_sid = "yoursid"
auth_token = "your_token"
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="desired_phone",
    from_="+18149628809",
    body="hi, this was sent from a python script!"
)

print(message.sid)