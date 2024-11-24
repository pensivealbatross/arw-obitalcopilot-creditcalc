import requests
import logging
logger = logging.getLogger(__name__)


# Deal with getting all the messages sent to Orbital Copilot in the current period
# Returns all messages in an array of dict
def get_messages():
    url = 'https://owpublic.blob.core.windows.net/tech-task/messages/current-period'

    response = requests.get(url)   #Make the get request to the endpoint
    # If the request was successfull return the messages, otherwise raise an exception as there's not a lot we can do without these messages
    if ( response.status_code == requests.codes.ok ):
        return response.json()['messages']
    else:
        raise Exception( 'Failed to get raw message data from Orbital Copilot. Messages endpoint returned status ' + str(response.status_code) )

# Deal with getting info about an Orbital Copilot report
# Expect a report id passed as an integer
# Returns dict of report info when present, None if not present
def get_report(id):
    url = 'https://owpublic.blob.core.windows.net/tech-task/reports'

    response = requests.get( url + '/' + str(id) )   #Make the get request to the endpoint
    if ( response.status_code == requests.codes.ok ):
        return response.json()
    elif ( response.status_code == 404 ):
        return None 
    else:
        raise Exception( 'Failed to get report [' + str(id) + ']. Reports endpoint returned status ' + str(response.status_code) )

def tests():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.info('Get messages: %s', get_messages() )
    logger.info('Resault for report %s: %s', 5392, get_report(5392) )  #report info present
    logger.info('Resault for report %s: %s', 9634, get_report(9634) )  #report info not present
