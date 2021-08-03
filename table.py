from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from httplib2 import Http


def table():
    services = {"bot": None}

    credentials = ServiceAccountCredentials._from_parsed_json_keyfile({
        "type": "service_account",
        "project_id": "calm-mariner-304222",
        "private_key_id": "bae60fb003764ede6e466a09164f45e6c8b859c2",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC4uhgiRMWUC/1B\n0zEbwhqXdPHSkgVP7zhZ56lHbs6C251deRGpHoXfYiIYAzGpKKa9BREgMOkmrO+2\np9z5jFhJG1GcUCUYLMhO1QQSxCghbaeN2f6p+4nlhO7S+YMnHS8MHoQOauHpbUsd\n4IBrLUoQnADtyPS6TKNBjwCXPeEAOQXS78wuHw8achGt23ORnvnx7E8wAzIdUvOQ\nwusn5zLpkmIDGZW77Wu5nV9l3xlcZhfyQuwlM+/6scoi+zDarMm+Z69Xlnj7I0Cc\n2gsTaxVSzQpr49nLYQj2BAZsKpvAwuEq0JppLqU6VtS8VvMQeXPp6EN4znHHLl2w\nP244wQTjAgMBAAECggEAQFPdr6FPRHzgVpna0hXH+NIqm+9plipx7yzzEAMQOxWL\nOU+9zKzqZZ3gzYffNU8IsW4gRpuBtYwnde4Cz4wF+n9e7hYitMZzgrA/WOGiL/Hl\nlUpCmqMTpC+kkyd8epR5G7lMt1CVFxqOO/s//RKqZhpNYIDIaE/j0iKgTAqqXc7m\nJ/mPDoMXepY0IkDyipnWsOTBgkzfO5aR1GawyCTgGEdM/pGqFHoDI0PO3YoNtrcR\nsZikGTgQ2wWlsKkBUyYgR+gHi2Qas70nJtNOAFOkLgcEHnp3w96TMVAN2Uy4HDiR\nfOH9ZRQ/7e57s1F/WHYd98RHJQ4sks5eZlJKnO+ogQKBgQDgEk9x1OfVsp8XN5lZ\nTBd/795fMdKx0e3lJb1FuchrTyyvoCbKwyiER2oWaoKo4+qi3e9lTXrcFS+CVYvv\nafPunh1VnVy67+tcs3aXKc+0xM9Z+zk0wN/iuGZgYaLPuVQpsGTaZb1gkluSrSpa\nZUmuVybAZLrA12WAgnQwmjndYQKBgQDTDJIBdlWCytqCHkIMgHuYIRwoC30kgoS9\nh+Owhp9fHNxQ7rr384p3cFPhhXUgK0ECymafNUXgMfuCLG/WzrTS+2eWu7uMGzz5\nEVEXk4ehDrqnP2TTaMr4KVfufUbJ16OwFLsv/pQCBhEuQHjGxaSVVyULLG0NSdk6\nRjeiOWPkwwKBgC2FSsJzYE3Xpd5Pm0W64aNKFcD9HDKn1U6SJit+HKtAQHHFdVwH\n3blR0MmRBc5NzyMbN0E7RlRjsW0m9/DBc57sXEVCXM5VY1lH1DXNdrbgrMc49Fw1\nOsaSc6ns6+iLW//EKBj+RkTSNuxLZalLnnZemi7Hx/DZUXOUDQq6qjrBAoGAem7J\naMXAN578gg2RnXUPviI/FlAL6hk5bkYd5XNDk0bH3L+RgXQsOLvWPXdRijbtgPPv\n8p5SCgyU7mBfBQtnRRoJbx07YL0QcyEDnRy9ysYjrBCPqkEZtjstwrG0VjWdxPFR\n4jbaoA3q+5z1M8LGhshGOiQso0/bD/5aGecXN0cCgYEAxRp49NS00rx+SDLJYZbz\ntNnqNf+rY+dfoYKU38S295sFiDLc9D67KfSevSNgPn8nWFS3/OCzd3UQnZjQU0l3\nmutoYSXEZPJyNtWm9hUOEJdC65sH6pL1FYkqS+pSkehlsOBwSvQdMSJGSYB1/i9H\naBIUGqmmq0aBs0fnltDa1ek=\n-----END PRIVATE KEY-----\n",
        "client_email": "sxa-1000@calm-mariner-304222.iam.gserviceaccount.com",
        "client_id": "113670012120547340229",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sxa-1000%40calm-mariner-304222.iam.gserviceaccount.com"
    },
        ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(Http())
    services["bot"] = discovery.build('sheets', 'v4', http=httpAuth)
    return services
