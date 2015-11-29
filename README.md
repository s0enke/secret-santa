# Secret Santa

This is a playground project in order to learn "future technologies" like
serverless/containerless applicaions with AWS Lambda etc. and some mathematical
theory.

It's a simple machine which creates a "Secret Santa" list and sends out mails to
participants.

## Setup

All setup (except SES outgoing mail) is automated with Ansible. It will use CloudFormation where possible.

### Deploy everything

```
source setup.sh
ansible-playbook deploy.yml
```

### Deploy fixtures to DynamoDB

Create a `fixtures.yml` looking like this:

```
---
user:
  - PutRequest:
      Item:
        id:
          S: soenke
  - PutRequest:
      Item:
        id:
          S: bernd
        blacklist:
          L:
            - S: werner
  - PutRequest:
      Item:
        id:
          S: werner
        blacklist:
          L:
            - S: bernd
  - PutRequest:
      Item:
        id:
          S: horst
        blacklist:
          L:
            - S: werner
            - S: soenke
```

Populate DynamoDB table:

```
source setup.sh
ansible-playbook load-fixtures.yml
```

## TODO

 - consistent naming
 - local development env
 - tests for the notifier
 - give it a nice GUI e.g. with API Gateway, React and co
 - Auth with Cognito/OIDC
 - make it entirely AWS region agnostic
 - Learn more theory (permutations, derangement etc.) and apply more mathematical terms
 - store and remember last "draws" (Ziehungen)

## Resources

### Theoretical background

 - https://www.lix.polytechnique.fr/~liberti/sesan.pdf
 - https://en.wikipedia.org/wiki/Derangement
