from flask import Flask
import orbitalcopilot
import calculatecost
import json
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# The /usage endpoint defined in Flask.
# This is the main endpoint, call it to calculate credits used
@app.route("/usage")
def calculate_usage():
    start_time = time.time()

    usage = []
    for message in orbitalcopilot.get_messages():
        logger.debug('Processing message %s', message)

        #Initial the message usage with the info that will always be available
        message_usage = {
            'message_id': message['id'],
            'timestamp': message['timestamp']
        }

        # The message may have a report id, if we need to include some information about it
        if ( 'report_id' in message ):
            # Get info about the report if it is available
            report = orbitalcopilot.get_report( message['report_id'] )

            if ( report != None ):
                #There was information about the report available. Add the report name and the cost provided to usage.
                message_usage['report_name'] = report['name']
                message_usage['credits_used'] = report['credit_cost']
            else:
                #No available information about the report. We treat this message as if it has no report and fall back to the credit calculator
                message_usage['credits_used'] = calculatecost.credits_by_message( message['text'] )
        else:
            #The message does not have a report id. Calculate the cost of this message using the credit calculator
            message_usage['credits_used'] = calculatecost.credits_by_message( message['text'] )

        usage.append( message_usage )

    end_time = time.time()
    logger.info('Usage report generated for %s messages in %s secconds', len(usage), (end_time - start_time) )

    return { 'usage': usage } # usage array must be enclosed in a dict to satisfy the service contract
