import boto3

def lambda_handler(event, context):
    donor = event['donor']
    receiver = event['receiver']
    to_email = '%s@ruempler.eu' % donor

    session = boto3.session.Session(region_name='us-east-1')
    client = session.client('ses')

    response = client.send_email(
        Source='Die Wichtelwuerfelmaschine <soenke@ruempler.eu>',
        Destination={
            'ToAddresses': [
                to_email,
            ],
        },
        Message={
            'Subject': {

                'Data': 'Deine Wichtelwahl 2016',
                },
            'Body': {
                'Text': {
                    'Data': "Hallo %s!\n\nDieses Jahr darfst du %s ein Geschenk machen! Gruss, deine automatische Wichtelmaschine." % (donor, receiver),
                },
            }
        },
    )
