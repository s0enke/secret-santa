import sys
import itertools
import random
import copy
import boto3
import json
from collections import defaultdict

def lambda_handler(event, context):

    dynamodb = boto3.client('dynamodb')

    wichtel_result = dynamodb.scan(
            TableName='user',
    )

    wichtel = []
    blacklist = {}

    for user in wichtel_result['Items']:
        user_id = user['id']['S']
        wichtel.append(user_id)
        print user['blacklist']['L']
        blacklist[user_id] = [blacklist_item['S'] for blacklist_item in user['blacklist']['L']]

# tuple permutations
    l = itertools.permutations(wichtel, 2)
    d = defaultdict(list)
    for v,k in l:
      d[k].append(v)

# blacklist anwenden
    possible_donations = {}
    for donor,receivers in d.items():
      a = set(receivers) - set(blacklist[donor])
      possible_donations[donor] =  list(a)
    print possible_donations

# integrity check (no empty possibilities)

# integrety check 2: no uniq receiver

# choose
    donations = {}
    for donor in d:
      print '------------'
      print donations
      print donor, possible_donations[donor]

      while True:

        receiver = random.choice(possible_donations[donor])

        new_possible_donations = copy.deepcopy(possible_donations)

#        print '===================='
#        print "possible donations: ", new_possible_donations
#        print "random choice for donor %s: %s" % (donor, receiver)

        del new_possible_donations[donor]
        found_empty_receiver = False
        for remaining_donor, remaining_receivers in new_possible_donations.items():
            try:
                new_possible_donations[remaining_donor].remove(receiver)
            except ValueError:
                pass

            if not len(new_possible_donations[remaining_donor]):
                print "empty remaining donor %s while choosing receiver for %s" % (remaining_donor, donor)
                found_empty_receiver = True
                break

        if found_empty_receiver:
            print "broken donations list (needs retry): ", new_possible_donations
            continue

        # TODO: check for deadlocks here, there MUST NOT be any equal lists

        possible_donations = new_possible_donations
        donations[donor] = receiver
        break

    print donations
    lambda_client = boto3.client('lambda')
    for donor,receiver in donations.items():
        response = lambda_client.invoke(
            FunctionName='wichtel-email',
            InvocationType="Event",
            Payload=json.dumps(
                {
                    "donor": donor,
                    "receiver": receiver,
                }
            ),
        )
