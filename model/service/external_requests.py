import logging
import os

import requests

from model.service.helpers import EXECUTION_APP_ENDPOINTS
from shared.utils.decorators import json_error_handler
from shared.utils.decorators import retry_failed_connection


@json_error_handler
@retry_failed_connection(num_times=3)
def execute_order(pipeline_id, signal, bearer_token, header=''):

    url = EXECUTION_APP_ENDPOINTS["EXECUTE_ORDER"](os.getenv("EXECUTION_APP_URL"))

    payload = {
        "pipeline_id": pipeline_id,
        "signal": signal,
    }

    position = "GO LONG" if signal == 1 else "GO SHORT" if signal == -1 else "GO NEUTRAL"

    logging.info(header + f"Sending {position} order with signal {signal}.")

    r = requests.post(url, json=payload, headers={"Authorization": bearer_token})
    logging.debug(r.text)

    response = r.json()
    logging.debug(response["message"])

    return response
