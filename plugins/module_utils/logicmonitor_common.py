# Copyright (c) 2022 LogicMonitor, Inc.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import hashlib
import hmac
import json
import socket
import time

# 3rd party imports
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def lmv1_authenticate(access_id, access_key, http_verb, resource_path, data=""):
    """
    Undergo LMv1 authentication process for REST API requests

    :param access_id: access ID token associated with the user's LM account
    :param access_key: access key token associated with the user's LM account
    :param http_verb: GET, PUT, POST, DELETE
    :param resource_path: REST resource endpoint
    :param data: data passed along with API requests
    :return: LMv1 token obtained after undergoing authentication
    """

    # Get current time in milliseconds
    epoch = str(int(time.time() * 1000))

    # Concatenate request details
    request_vars = http_verb + epoch + data + resource_path

    # Construct signature
    h = hmac.new(access_key.encode(), msg=request_vars.encode(), digestmod=hashlib.sha256).hexdigest()
    signature = base64.b64encode(h.encode())

    # Construct token
    return 'LMv1 ' + access_id + ':' + signature.decode() + ':' + epoch


def convert_date_to_timestamp(time_str):
    time_str = time_str.lower()
    if time_str.endswith("am") or time_str.endswith("pm"):
        template = "%Y-%m-%d %I:%M %p"
    else:
        template = "%Y-%m-%d %H:%M"
    return int(time.mktime(time.strptime(time_str, template)) * 1000)


class LogicMonitorBaseModule(object):
    """ Initialize the LogicMonitor base object """

    """URLS"""
    LM_BASE_URL = "logicmonitor.com/santaba/rest"
    DOWNLOAD_COLLECTOR_URL = "/setting/collector/collectors/{id}/bootstraps/Linux{arch}"
    COLLECTORS_BASE_URL = "/setting/collector/collectors"
    COLLECTOR_GROUPS_BASE_URL = "/setting/collector/groups"
    DEVICES_BASE_URL = "/device/devices"
    DEVICE_GROUPS_BASE_URL = "/device/groups"
    DEVICE_GROUP_DEVICES_BASE_URL = "/device/groups/{group_id}/devices"
    DEVICE_DATASOURCES_BASE_URL = "/device/devices/{device_id}/devicedatasources"
    ESCALATION_CHAINS_BASE_URL = "/setting/alert/chains"
    ALERT_RULE_BASE_URL = "/setting/alert/rules"
    RECIPIENT_URL = "/setting/recipients"
    SDT_URL = "/sdt/sdts"
    OPS_NOTE_BASE_URL = "/setting/opsnotes"
    WEBSITE_BASE_URL = "/website/websites"

    """QUERY PARAMETER TOKENS"""
    FILTER = "filter"
    SORT = "sort"
    SIZE = "size"
    OPERATION_TYPE = "opType"

    """MODULE ACTIONS"""
    ADD = "add"
    UPDATE = "update"
    REMOVE = "remove"
    SDT = "sdt"

    """REQUEST METHODS"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

    """FIELD NAMES"""
    ID = "id"
    DESCRIPTION = "description"
    TOTAL = "total"
    ITEMS = "items"
    NAME = "name"
    VALUE = "value"
    PARENT_ID = "parentId"
    ERROR_CODE = "errorCode"
    ERROR_MESSAGE = "errorMessage"
    ERROR_DETAIL = "errorDetail"

    def __init__(self, module):
        self.__version__ = "1.0-python"
        self.utils = DeviceUtils(self)
        self.module = module
        self.params = module.params
        self.module.debug("Instantiating LogicMonitor object")

        self.change = False
        self.check_mode = False

        if self.ModuleFields.ACTION in self.params:
            self.action = self.params[self.ModuleFields.ACTION]
        self.company = self.params[self.ModuleFields.COMPANY]
        self.access_id = self.params[self.ModuleFields.ACCESS_ID]
        self.access_key = self.params[self.ModuleFields.ACCESS_KEY]
        self.fqdn = socket.getfqdn()
        self.__version__ = self.__version__ + "-ansible-module"

        self.lmotel_collector_utils = self.create_lmotel_collector_utils()
        self.collector_utils = self.create_collector_utils()
        self.collector_group_utils = self.create_collector_group_utils()
        self.device_utils = self.create_device_utils()
        self.device_group_utils = self.create_device_group_utils()
        self.escalation_chain_utils = self.create_escalation_chain_utils()
        self.alert_rule_utils = self.create_alert_rule_utils()
        self.recipient_utils = self.create_recipient_utils()
        self.website_check_utils = self.create_website_check_utils()
        self.ops_note_utils = self.create_ops_note_utils()

        if not HAS_REQUESTS:
            self.fail(
                "This module requires the python 'requests' package."
                "Try `pip install requests` if using Python 2 or `pip3 install requests` if using Python 3.")

    def create_lmotel_collector_utils(self):
        return LmotelCollectorUtils(self)

    def create_collector_utils(self):
        return CollectorUtils(self)

    def create_collector_group_utils(self):
        return CollectorGroupUtils(self)

    def create_device_utils(self):
        return DeviceUtils(self)

    def create_device_group_utils(self):
        return DeviceGroupUtils(self)

    def create_escalation_chain_utils(self):
        return EscalationChainUtils(self)

    def create_alert_rule_utils(self):
        return AlertRuleUtils(self)

    def create_recipient_utils(self):
        return RecipientUtils(self)

    def create_website_check_utils(self):
        return WebsiteCheckUtils(self)

    def create_ops_note_utils(self):
        return OpsNoteUtils(self)

    def process_field(self, original_val, new_val=""):
        """
        Return the default value for an associated field if it's empty
        :param original_val: original value of field to check
        :param new_val: default value of field to return if empty
        :return: original value of field (if not empty) or the default value
        """
        self.module.debug("Running LogicMonitorBaseModule.process_field...")
        if original_val is None:
            return new_val
        elif isinstance(original_val, str):
            # remove leading/trailing whitespace
            original_val = original_val.strip()
            if not original_val:
                return new_val
        return original_val
    
    def paginated_request(self, url, query_params=None, err_msg=""):
        """
        Make paginated requests to LogicMonitor REST API
        :param url: REST resource endpoint
        :param query_params: query parameter map (e.g. {filter: x}) passed along with API request
        :param err_msg: error message to display to a user if an error occurs
        :return: dictionary containing 'items' (list of all items) and 'total' (total count of items)
        """
        self.module.debug("Running LogicMonitorBaseModule.paginated_request...")

        if query_params is None:
            query_params = {}

        all_items = []
        offset = 0
        total = None
        page_size = min(self.size, 1000)  # Use the specified size, but cap it at 1000
        max_iterations = 1000  # Safety mechanism to prevent infinite loops

        for iteration in range(max_iterations):
            current_params = query_params.copy()
            current_params['offset'] = offset
            current_params['size'] = page_size

            self.module.debug(f"Making request with params: {current_params}")
            response = self.rest_request(self.GET, url, query_params=current_params, err_msg=err_msg)

            if not self.success_response(response):
                self.fail(f"{err_msg}\nResponse: {str(response)}")

            items = response.get('items', [])
            all_items.extend(items)

            if total is None:
                total = response.get('total', 0)
                self.module.debug(f"Total items reported by API: {total}")

            self.module.debug(f"Iteration {iteration + 1}: Fetched {len(items)} items. Total items so far: {len(all_items)}.")

            if len(items) == 0 or len(all_items) >= total:
                self.module.debug("Pagination complete.")
                break

            offset += len(items)

        else:
            self.module.warn(f"Reached maximum number of iterations ({max_iterations}). "
                            f"Total items fetched: {len(all_items)}, Expected total: {total}")
            self.module.debug(f"Last response: {response}")

        return {
            'items': all_items,
            'total': total
        }

    def rest_request(self, http_verb, resource_path, data="", path_params="" ,query_params=None, err_msg="", fail_module=True, collector_type=""):
        """
        Make request to LogicMonitor REST API
        :param http_verb: GET, PUT, POST, DELETE
        :param resource_path: REST resource endpoint
        :param data: data passed along with API request
        :param path_params: parameters to be passed alongside url (e.g. download collector)
        :param query_params: query parameter map (e.g. {filter: x}) passed along with API request
        :param err_msg: error message to display to a user if an error occurs
        :param fail_module: denotes whether or not module should fail if the request fails
        :param collector-type: collecter type for deciding X-version for the header
        :return: result obtained from API requests
        """
        self.module.debug("Running LogicMonitorBaseModule.rest_request...")

        company = self.module.params[self.ModuleFields.COMPANY].lower()
        access_id = self.module.params[self.ModuleFields.ACCESS_ID]
        access_key = self.module.params[self.ModuleFields.ACCESS_KEY]
        url = "https://" + company + "." + self.LM_BASE_URL + resource_path + path_params

        if data or data == {}:
            data = json.dumps(data)

        if query_params is None:
            query_params = {}

        response = None
        try:
            lmv1_token = lmv1_authenticate(access_id, access_key, http_verb, resource_path, data)
            # Set headers
            headers = {
                "Authorization": lmv1_token,
                "X-Version": "3",
                "Content-Type": "application/json"
            }

            if collector_type == "lmotel":
                headers["X-Version"] = "4"

            # Disable SSL certification for localdev API requests
            ssl_cert = True
            if company == "localdev":
                ssl_cert = False

            if http_verb == self.GET:
                req = requests.get
            elif http_verb == self.POST:
                req = requests.post
            elif http_verb == self.PUT:
                req = requests.put
            elif http_verb == self.PATCH:
                req = requests.patch
            elif http_verb == self.DELETE:
                req = requests.delete
            else:
                raise Exception("Invalid request method: " + http_verb)
            
            response = req(url, data=data, params=query_params, headers=headers, verify=ssl_cert)
            json_resp = json.loads(response.content)
            self.handle_failed_response(response.status_code, json_resp, err_msg, fail_module)
            return json_resp
        except ValueError as ve:
            self.module.debug(
                "Response received from LogicMonitor is not JSON-formatted\nResponse: " +
                str(response) + "\nException: " + str(ve))
            if response:
                self.handle_failed_response(response.status_code, response.content, err_msg)
                return response.content
            else:
                self.fail(msg=err_msg + " \nException: " + str(ve))
        except Exception as ex:
            self.module.debug(msg="Error: Exception making REST API call to " + url + "\nException: " + str(ex))
            self.fail(err_msg + "\nException: " + str(ex))

    def handle_failed_response(self, status_code, response, err_msg, fail_module=True):
        """
        Parse LogicMonitor api response for any errors and display them accordingly to the user
        :param status_code: status code of API response
        :param response: response body of API response
        :param err_msg: error message to display to a user if an error is caught
        :param fail_module: denotes whether or not module should fail if an error occurs
        """
        self.module.debug("Running LogicMonitorBaseModule.handle_failed_response...")
        if status_code != 200:
            if status_code == 401 or status_code == 1401:
                self.fail(
                    "Authentication failure - Invalid credentials. "
                    "Make sure your access_id & access_key credentials are valid\n"
                    "Response: " + str(response))
            else:
                self.handle_module_err(err_msg + " \nResponse: " + str(response), fail_module)

    def handle_module_err(self, err_msg, fail_module=True):
        self.module.debug("Running LogicMonitorBaseModule.handle_module_err...")
        if fail_module:
            self.fail(str(err_msg))
        else:
            self.module.debug(str(err_msg))

    def success_response(self, resp):
        self.module.debug("Running LogicMonitorBaseModule.success_response...")
        return resp and self.ERROR_CODE not in resp

    def build_properties(self, properties):
        """
        Return JSONArray containing key-value pairings of custom properties provided when
        adding/updating an LM device or device group.
        Return empty JSONArray if no custom properties are provided
        """
        self.module.debug("Running LogicMonitorBaseModule.build_properties...")
        if properties is None:
            properties = {}

        props = []
        if properties:
            for key, value in properties.items():
                if not value:
                    value = ""
                elif isinstance(value, list):
                    value = ",".join(map(str, value))
                prop = {
                    self.NAME: key,
                    self.VALUE: value
                }
                props.append(prop)
        return props

    def get_sdt_interval(self, start_time, end_time, duration):
        """ Retrieve the SDT start & end epoch timestamps

        :param start_time: the start time of the SDT
               - formatted as 'yyyy-MMM-dd HH:mm' or 'yyyy-MM-dd HH:mm z'
        :param end_time: the end time of the SDT
               - formatted as 'yyyy-MMM-dd HH:mm' or 'yyyy-MM-dd HH:mm z'
        :param duration: the duration of the SDT
        :return: List containing the integer epoch timestamps corresponding to the SDT start & end time, respectively
        """
        self.module.debug("Running LogicMonitor.get_sdt_interval...")

        try:
            start_ts = self.get_sdt_start_time(start_time)
            end_ts = self.get_sdt_end_time(start_ts, end_time, duration)
        except ValueError as ex:
            self.fail(
                "Failed to parse start_time or end_time provided. Please make sure the time provided is formatted as "
                "'yyyy-MMM-dd HH:mm' or 'yyyy-MM-dd HH:mm z' \nException: " + str(ex))

        if start_ts >= end_ts:
            self.fail("The SDT end_time must be greater than the start_time.")
        return [start_ts, end_ts]

    def get_sdt_start_time(self, start_time):
        """ Retrieve the SDT start epoch timestamp

        :param start_time: the start time of the SDT
               - formatted as 'yyyy-MMM-dd HH:mm' or 'yyyy-MM-dd HH:mm z'
        :return: integer epoch timestamp that corresponds to the sdt start time
        """
        self.module.debug("Running LogicMonitor.get_sdt_start_time...")

        if start_time:
            self.module.debug("Start time specified")
            return convert_date_to_timestamp(start_time)
        else:
            self.module.debug("No start time specified. Using default.")
            return int(time.time() * 1000)

    def get_sdt_end_time(self, start_ts, end_time, duration):
        """ Retrieve the SDT end epoch timestamp

        :param start_ts: the epoch timestamp representing the SDT start time
        :param end_time: the end time of the SDT
               - formatted as 'yyyy-MMM-dd HH:mm' or 'yyyy-MM-dd HH:mm z'
        :param duration: the duration of the SDT
        :return: integer epoch timestamp that corresponds to the sdt end time
        """
        self.module.debug("Running LogicMonitor.get_sdt_end_time...")

        if end_time:
            self.module.debug("End time specified")
            return convert_date_to_timestamp(end_time)
        else:
            self.module.debug("No end time specified. Using duration.")
            if duration <= 0:
                self.fail("SDT duration must be greater than 0")
            return start_ts + (duration * 60000)
    
    def get_ops_note_time(self, note_time):
        self.module.debug("Running LogicMonitor.get_ops_note_time...")
        if note_time:
            return convert_date_to_timestamp(note_time)
        else:
            return int(time.time() * 1000)

    def parse_filter_request_response(self, resp):
        self.module.debug("Running LogicMonitor.parse_filter_request_response...")
        if self.TOTAL in resp:
            num_items = resp[self.TOTAL]
            if num_items > 0:
                return resp[self.ITEMS][0]
        else:
            return resp

    def is_int(self, num):
        self.module.debug("Running LogicMonitor.is_int...")
        try:
            int(num)
            return True
        except ValueError:
            return False

    def valid_id(self, id):
        self.module.debug("Running LogicMonitor.valid_id...")
        return id is not None and id > 0

    def fail(self, msg):
        self.module.fail_json(msg="Error: " + str(msg), changed=self.change, failed=True)

    def exit(self):
        self.module.debug("Changed: " + str(self.change))
        self.module.exit_json(changed=self.change, success=True)

    def exit_with_info(self):
        self.module.debug("Changed: " + str(self.changed))
        self.module.exit_json(changed=self.changed, success=True, data=self.result,
                              action_performed=self.action_performed, additional_info=self.additional_info)

    def output_info(self, info):
        self.module.debug("Registering properties as Ansible facts")
        self.module.exit_json(changed=False, ansible_facts=info)

    class ModuleFields:
        TARGET = "target"
        ACTION = "action"
        COMPANY = "company"
        ACCESS_ID = "access_id"
        ACCESS_KEY = "access_key"

        ID = "id"
        DESCRIPTION = "description"
        INSTALL_PATH = "install_path"
        INSTALL_USER = "install_user"
        COLLECTOR_GROUP_ID = "collector_group_id"
        COLLECTOR_GROUP_NAME = "collector_group_name"
        DEVICE_GROUP_ID = "device_group_id"
        DEVICE_GROUP_FULL_PATH = "device_group_full_path"
        PLATFORM = "platform"
        VERSION = "version"
        SIZE = "size"

        DISPLAY_NAME = "display_name"
        HOSTNAME = "hostname"
        COLLECTOR_ID = "collector_id"
        COLLECTOR_DESCRIPTION = "collector_description"
        GROUPS = "groups"
        DISABLE_ALERTING = "disable_alerting"
        PROPERTIES = "properties"

        AUTO_BALANCE = "auto_balance"
        INSTANCE_THRESHOLD = "instance_threshold"

        FULL_PATH = "full_path"
        DATASOURCE_ID = "datasource_id"
        DATASOURCE_NAME = "datasource_name"

        NAME = "name"
        DEVICE_ID = "device_id"
        DEVICE_DISPLAY_NAME = "device_display_name"
        DEVICE_HOSTNAME = "device_hostname"

        START_TIME = "start_time"
        END_TIME = "end_time"
        DURATION = "duration"
        COMMENT = "comment"

        FORCE_MANAGE = "force_manage"

        BACKUP_COLLECTOR_ID = "backup_collector_id"
        BACKUP_COLLECTOR_DESCRIPTION = "backup_collector_description"
        RESEND_IVAL = "resend_collector_down_alert_interval"
        ESCALATING_CHAIN_ID = "escalating_chain_id"
        ESCALATING_CHAIN_NAME = "escalating_chain_name"

        OPTYPE = "optype"
        OPTYPE_REFRESH = "refresh"
        OPTYPE_REPLACE = "replace"
        OPTYPE_ADD = "add"

        PRIORITY = "priority"
        LEVEL = "level"
        DEVICES = "devices"
        DATASOURCE = "datasource"
        DATAPOINT = "datapoint"
        INSTANCE = "instance"
        SUPPRESS_CLEAR = "suppress_clear"
        SUPPRESS_ACK_AND_SDT = "suppress_ACK_STD"
        ESCALATION_CHAIN_ID = "escalation_chain_id"
        ESCALATION_INTERVAL = "escalation_interval"
        RESOURCE_PROPERTIES = "resource_properties_filter"

        ENABLE_THROTTLING = "enable_throttling"
        RATE_LIMIT_ALERTS = "rate_limit_alerts"
        RATE_LIMIT_PERIOD = "rate_limit_period"
        CC_DESTINATIONS = "cc_destinations"
        DESTINATIONS = "destinations"

        WEBSITE_CHECK_ID = "website_check_id"
        WEBSITE_CHECK_NAME = "website_check_name"
        CHECKPOINT_ID = "checkpoint_id"
        CHECKPOINT_NAME = "checkpoint_name"

        NOTE_TIME = "note_time"
        NOTE = "note"
        TAGS = "tags"
        SCOPES = "scopes"
        SCOPE_TYPE = "scope_type"

    class OpsNoteFields:
        OPS_NOTE_ID = "id"
        OPS_NOTE_TAGS = "tags"
        OPS_NOTE_HAPPENED_ON_IN_SECONDS = "happenedOnInSec"
        OPS_NOTE_SCOPES = "scopes"
        NOTE = "note"

    class SDTFields:
        TYPE = "type"
        SDT_TYPE = "sdtType"
        START_DATE_TIME = "startDateTime"
        END_DATE_TIME = "endDateTime"
        COMMENT = "comment"
        ONE_TIME = "oneTime"
        COLLECTOR_SDT = "CollectorSDT"
        RESOURCE_SDT = "ResourceSDT"
        RESOURCE_GROUP_SDT = "ResourceGroupSDT"
        DEVICE_DATASOURCE_SDT = "DeviceDataSourceSDT"
        WEBSITE_SDT = "WebsiteSDT"
        WEBSITE_CHECKPOINT_SDT = "WebsiteCheckpointSDT"
        WEBSITE_ID = "websiteId"
        WEBSITE_NAME = "websiteName"
        START_DATE_TIME_ON_LOCAL = "startDateTimeOnLocal"
        END_DATE_TIME_ON_LOCAL = "endDateTimeOnLocal"
        SDT_ID = "sdt_id"

    class ALERTRULEFields:
        ID = "id"
        NAME = "name"
        PRIORITY = "priority"
        LEVEL = "levelStr"
        GROUPS = "deviceGroups"
        DEVICES = "devices"
        DATAPOINT = "datapoint"
        DATASOURCE = "datasource"
        INSTANCE = "instance"
        SUPPRESS_CLEAR = "suppressAlertClear"
        SUPPRESS_ALERT_ACK_SDT = "suppressAlertAckSdt"
        ESCALATION_CHAIN_ID = "escalatingChainId"
        ESCALATION_INTERVAL = "escalationInterval"
        RESOURCE_PROPERTIES = "resourceProperties"

    class ESCALATIONCHAINFields:
        ID = "id"
        NAME = "name"
        ENABLE_THROTTLING = "enableThrottling"
        THROTTLING_ALERTS = "throttlingAlerts"
        THROTTLING_PERIOD = "throttlingPeriod"
        CC_DESTINATIONS = "ccDestinations"
        DESTINATIONS = "destinations"
        DESCRIPTION = "description"

class LmotelCollectorUtils(object):

    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_collector_id(self, id, desc):
        self.lm.module.debug("Running LmotelCollectorUtils.get_collector_id...")
        resp = self.get_collector_info(id, desc)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_collector_info(self, id, fail_module=True):
        """
        Retrieve JSON object representation of a collector via group its ID or description
        :param id: collector ID
        :param fail_module: denotes whether or not module should fail if the collector isn't retrieved
        :return: JSONObject when successful; None when the collector doesn't exist; error message when retrieval fails
        """
        self.lm.module.debug("Running CollectorUtils.get_collector_info...")
        err_msg = "Failed to retrieve collector \nResponse: "

        # try getting collector by ID
        resp = self.get_collector_by_id(id, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Collector doesn't exist"
            else:
                err_msg = err_msg + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_collector_by_id(self, id, fail_module=True):
        """
        Get JSONObject representing collector via its ID.
        Return None if the collector doesn't exist.
        :param id: collector ID
        :param fail_module: denotes whether or not module should fail if collector isn't retrieved
        :return: JSONObject or None if collector doesn't exist and module hasn't failed
        """
        self.lm.module.debug("Running LmotelCollectorUtils.get_collector_by_id...")
        err_msg = "Failed to retrieve collector '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.COLLECTORS_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
        if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                and resp[self.lm.ERROR_MESSAGE].startswith("No such Agent"):
            resp = None
        return resp

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running LmotelCollectorUtils.send_patch_request...")
        url = self.lm.COLLECTORS_BASE_URL + "/" + str(id)
        err_msg = "Failed to update collector"
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module)

class CollectorUtils(object):

    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_collector_id(self, id, desc):
        self.lm.module.debug("Running CollectorUtils.get_collector_id...")
        resp = self.get_collector_info(id, desc)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_collector_info(self, id, desc, fail_module=True):
        """
        Retrieve JSON object representation of a collector via group its ID or description
        :param id: collector ID
        :param desc: collector description
        :param fail_module: denotes whether or not module should fail if the collector isn't retrieved
        :return: JSONObject when successful; None when the collector doesn't exist; error message when retrieval fails
        """
        self.lm.module.debug("Running CollectorUtils.get_collector_info...")
        err_msg = "Failed to retrieve collector \nResponse: "

        # try getting collector by ID
        resp = self.get_collector_by_id(id, False)
        if not self.lm.success_response(resp) and desc is not None:
            # try getting collector by description if unable to via ID
            resp = self.get_collector_by_description(desc, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Collector doesn't exist"
            else:
                err_msg = err_msg + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_collector_by_id(self, id, fail_module=True):
        """
        Get JSONObject representing collector via its ID.
        Return None if the collector doesn't exist.
        :param id: collector ID
        :param fail_module: denotes whether or not module should fail if collector isn't retrieved
        :return: JSONObject or None if collector doesn't exist and module hasn't failed
        """
        self.lm.module.debug("Running CollectorUtils.get_collector_by_id...")
        err_msg = "Failed to retrieve collector '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.COLLECTORS_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
        if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                and resp[self.lm.ERROR_MESSAGE].startswith("No such Agent"):
            resp = None
        return resp

    def get_collector_by_description(self, desc, fail_module=True):
        self.lm.module.debug("Running Collector_Utils.get_collector_by_description...")

        if desc is not None:
            query_filter = 'description:"{desc}"'.format(desc=desc)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve collector by description"
            resp = self.lm.rest_request(self.lm.GET, self.lm.COLLECTORS_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_collectors(self):
        self.lm.module.debug("Running CollectorUtils.get_collectors...")
        err_msg = "Failed to retrieve collectors"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.COLLECTORS_BASE_URL, query_params=query_params, err_msg=err_msg)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running Collector.send_patch_request...")
        url = self.lm.COLLECTORS_BASE_URL + "/" + str(id)
        err_msg = "Failed to update collector"
        query_params = {self.lm.OPERATION_TYPE: self.lm.optype}
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module, query_params=query_params)

class CollectorGroupUtils(object):

    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_collector_group_id(self, id, name):
        self.lm.module.debug("Running CollectorGroupUtils.get_collector_group_id...")
        resp = self.get_collector_group_info(id, name)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_collector_group_info(self, id, name, fail_module=True):
        """
        Retrieve JSON object representation of a collector group via its ID or name
        :param id: collector group ID
        :param name: collector group name
        :param fail_module: denotes whether or not module should fail if the collector group isn't retrieved
        :return: JSONObject when successful; None when the collector group doesn't exist; error message when retrieval
                 fails
        """
        self.lm.module.debug("Running CollectorGroupUtils.get_collector_group_info...")
        err_msg = "Failed to retrieve collector group \nResponse: "

        # try getting collector group by ID
        resp = self.get_collector_group_by_id(id, False)
        if not self.lm.success_response(resp) and name is not None:
            # try getting collector group by name if unable to via ID
            resp = self.get_collector_group_by_name(name, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Collector group doesn't exist"
            else:
                err_msg = err_msg + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_collector_group_by_id(self, id, fail_module=True):
        """
        Get JSONObject representing collector group via its ID.
        Return None if the collector group doesn't exist.
        :param id: collector group ID
        :param fail_module: denotes whether or not module should fail if collector group isn't retrieved
        :return: JSONObject or None if collector group doesn't exist and module hasn't failed
        """
        self.lm.module.debug("Running CollectorGroupUtils.get_collector_group_by_id...")
        err_msg = "Failed to retrieve collector group '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.COLLECTOR_GROUPS_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
        if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                and resp[self.lm.ERROR_MESSAGE].startswith("The requested group does not exist"):
            resp = None
        return resp

    def get_collector_group_by_name(self, name, fail_module=True):
        self.lm.module.debug("Running CollectorGroupUtils.get_collector_group_by_name...")

        if name is not None:
            if name.strip() == "":
                name = "@default"
            query_filter = 'name:"{name}"'.format(name=name)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve collector group by name"
            resp = self.lm.rest_request(self.lm.GET, self.lm.COLLECTOR_GROUPS_BASE_URL, query_params=query_params,
                                        err_msg=err_msg)
            return self.lm.parse_filter_request_response(resp)

    def get_collector_groups(self):
        self.lm.module.debug("Running CollectorGroupUtils.get_collector_groups...")
        err_msg = "Failed to retrieve collector groups"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.COLLECTOR_GROUPS_BASE_URL, query_params=query_params,
                                    err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running CollectorGroupUtils.send_create_request...")
        err_msg = "Failed to create collector group"
        return self.lm.rest_request(self.lm.POST, self.lm.COLLECTOR_GROUPS_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running CollectorGroup.send_patch_request...")
        url = self.lm.COLLECTOR_GROUPS_BASE_URL + "/" + str(id)
        err_msg = "Failed to update collector group"
        query_params = {self.lm.OPERATION_TYPE: self.lm.optype}
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module, query_params=query_params)

    def send_delete_request(self, id, fail_module=True):
        self.lm.module.debug("Running CollectorGroupUtils.send_delete_request...")
        err_msg = "Failed to delete collector group " + str(id)
        self.lm.rest_request(self.lm.DELETE, self.lm.COLLECTOR_GROUPS_BASE_URL + '/' + str(id), err_msg=err_msg,
                             fail_module=fail_module)

class DeviceUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_device_id(self, id, display_name="", hostname=""):
        self.lm.module.debug("Running DeviceUtils.get_device_id...")
        resp = self.get_device_info(id, display_name, hostname)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_device_info(self, id, display_name, hostname, fail_module=True):
        """
        Retrieve JSON object representation of a device via its ID, display_name, or hostname
        :param id: device ID
        :param display_name: device display name
        :param hostname: device hostname (name)
        :param fail_module: denotes whether or not module should fail if the device isn't retrieved
        :return: JSONObject when successful; None when the device doesn't exist; error message when retrieval fails
        """
        self.lm.module.debug("Running DeviceUtils.get_device_info...")

        # try getting device by ID
        resp = self.get_device_by_id(id, False)
        if not self.lm.success_response(resp) and (display_name or hostname):
            # try getting device by name if unable to via ID
            resp = self.get_device_by_name(display_name, hostname, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Device doesn't exist"
            else:
                err_msg = "Failed to retrieve device \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_device_by_id(self, id, fail_module=True):
        """
        Get JSONObject representing device via its ID. Return None if the device doesn't exist.
        :param id: device ID
        :param fail_module: denotes whether or not module should fail if device isn't retrieved
        :return: JSONObject or None if device doesn't exist and module hasn't failed
        """
        self.lm.module.debug("Running DeviceUtils.get_device_by_id...")
        err_msg = "Failed to retrieve device '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.DEVICES_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].startswith("Resource not found"):
                resp = None
        return resp

    def get_device_by_name(self, display_name, hostname, fail_module=True):
        self.lm.module.debug("Running DeviceUtils.get_device_by_name...")

        if display_name is not None or hostname is not None:
            if display_name is not None and hostname is not None:
                query_filter = 'displayName:"{dn}"||name:"{hn}"'.format(dn=display_name, hn=hostname)
            elif display_name is not None:
                query_filter = 'displayName:"{dn}"'.format(dn=display_name)
            else:
                query_filter = 'name:"{hn}"'.format(hn=hostname)

            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve device by name"
            resp = self.lm.rest_request(self.lm.GET, self.lm.DEVICES_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_devices(self):
        self.lm.module.debug("Running DeviceUtils.get_devices...")
        err_msg = "Failed to retrieve devices"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.DEVICES_BASE_URL, query_params=query_params, err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running Device.send_create_request...")
        err_msg = "Failed to create device"
        return self.lm.rest_request(self.lm.POST, self.lm.DEVICES_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running Device.send_patch_request...")
        url = self.lm.DEVICES_BASE_URL + "/" + str(id)
        err_msg = "Failed to update device"
        query_params = {self.lm.OPERATION_TYPE: self.lm.optype}
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module, query_params=query_params)

class DeviceGroupUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_device_group_id(self, id, full_path):
        self.lm.module.debug("Running DeviceGroupUtils.get_device_group_id...")
        resp = self.get_device_group_info(id, full_path)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_device_group_devices(self, group_id):
        self.lm.module.debug("Running DeviceGroupUtils.get_device_group_devices...")
        err_msg = "Failed to retrieve device group devices"
        url = self.lm.DEVICE_GROUP_DEVICES_BASE_URL.format(group_id=group_id)
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(url, query_params=query_params, err_msg=err_msg)

    def get_device_group_info(self, id, full_path, fail_module=True):
        """
        Retrieve JSON object representation of a device group via its ID or full_path
        :param id: device group ID
        :param full_path: device group full path
        :param fail_module: denotes whether or not module should fail if the device group isn't retrieved
        :return: JSONObject when successful; None when the device group doesn't exist; error message when retrieval
                 fails
        """
        self.lm.module.debug("Running DeviceGroupUtils.get_device_group_info...")

        # try getting device group by ID
        resp = self.get_device_group_by_id(id, False)
        if not self.lm.success_response(resp) and full_path is not None:
            # try getting device by full_path if unable to via ID
            resp = self.get_device_group_by_full_path(full_path, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Device group doesn't exist"
            else:
                err_msg = "Failed to retrieve device group \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_device_group_by_id(self, id, fail_module=True):
        """
        Get JSONObject representing device group via its ID.
        Return None if the device doesn't exist.
        :param id: device group ID
        :param fail_module: denotes whether or not module should fail if device group isn't retrieved
        :return: JSONObject or None if device group doesn't exist and module hasn't failed
        """
        self.lm.module.debug("Running DeviceGroupUtils.get_device_group_by_id...")
        err_msg = "Failed to retrieve device group '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            self.lm.module.debug("Running get_device_group_by_id...")
            url = self.lm.DEVICE_GROUPS_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].endswith("is not found."):
                resp = None
        return resp

    def get_device_group_by_full_path(self, full_path, fail_module=True):
        """
        Retrieve the device group via its full path.
        :param full_path: full path corresponding to group
        :param fail_module: denotes whether or not module should fail if a group isn't retrieved
        :return: JSON object representation of device group
        """
        self.lm.module.debug("Running DeviceGroupUtils.get_device_group_by_full_path...")

        if full_path is not None:
            full_path = full_path.strip().strip("/")
            query_filter = 'fullPath:"{fp}"'.format(fp=full_path)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve device group by full path"
            resp = self.lm.rest_request(self.lm.GET, self.lm.DEVICE_GROUPS_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_device_groups(self):
        self.lm.module.debug("Running DeviceGroupUtils.get_device_groups...")
        err_msg = "Failed to retrieve device groups"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.DEVICE_GROUPS_BASE_URL, query_params=query_params,
                                    err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running DeviceGroupUtils.send_create_request...")
        err_msg = "Failed to create device group"
        return self.lm.rest_request(self.lm.POST, self.lm.DEVICE_GROUPS_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running DeviceGroup.send_patch_request...")
        url = self.lm.DEVICE_GROUPS_BASE_URL + "/" + str(id)
        err_msg = "Failed to update device group"
        query_params = {self.lm.OPERATION_TYPE: self.lm.optype}
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module, query_params=query_params)

    def check_group_path(self, full_path):
        """
        Check if device group full path is invalid - i.e. it contains spaces or consecutive slashes ('/')
        """
        self.lm.module.debug("Running DeviceGroupUtils.check_group_path...")
        full_path = full_path.strip()
        if " /" in full_path or "/ " in full_path or "//" in full_path:
            self.lm.fail("Invalid group path: '" + full_path + "'")

    def get_new_or_existing_group_id(self, full_path):
        """
        Get the the ID of device group denoted by the full_path. If the full_path corresponds to a non-existent group,
        we recursively create the group (and parents groups) and return the ID of the newly created group.
        The full_path must be formatted correctly - i.e.
        (1) isn't null
        (2) doesn't contain empty group names
        (3) doesn't end in a slash "/"
        (4) no whitespace between group names and slashes - e.g. "a / b"
        :param full_path: full path that corresponds to new or existing group
        :return: ID of existing or newly created group
        """
        self.lm.module.debug("Running DeviceGroupUtils.get_new_or_existing_group_id...")

        full_path = full_path.strip()
        if full_path == "" or full_path == "/":
            return 1
        else:
            device_group = self.get_device_group_by_full_path(full_path)
            if device_group:
                return device_group[self.lm.ID]
            else:
                parent_path, name = full_path.rsplit("/", 1)
                if parent_path == "":
                    parent_id = 1
                else:
                    parent_group = self.get_device_group_by_full_path(parent_path)
                    if parent_group:
                        parent_id = parent_group["id"]
                    else:
                        parent_id = self.get_new_or_existing_group_id(parent_path)

                data = {
                    self.lm.NAME: name.strip(),
                    self.lm.PARENT_ID: parent_id
                }

                existing_group = self.get_device_group_by_full_path(full_path)
                if existing_group:
                    return existing_group[self.lm.ID]
                else:
                    new_group = self.send_create_request(data)
                    return new_group[self.lm.ID]

class EscalationChainUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_escalation_chain_id(self, id, name):
        self.lm.module.debug("Running EscalationChainUtils.get_escalation_chain_id...")
        resp = self.get_escalation_chain_info(id, name)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_escalation_chain_info(self, id, name, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.get_escalation_chain_info...")

        # try getting escalation cain by ID
        resp = self.get_escalation_chain_by_id(id, False)
        if not self.lm.success_response(resp) and name is not None:
            # try getting escalation chain by name if unable to via ID
            resp = self.get_escalation_chain_by_name(name, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Escalation chain doesn't exist"
            else:
                err_msg = "Failed to retrieve escalation chain \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_escalation_chain_by_id(self, id, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.get_escalation_chain_by_id...")
        err_msg = "Failed to retrieve escalation chain '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.ESCALATION_CHAINS_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].startswith("No such chain"):
                resp = None
        return resp

    def get_escalation_chain_by_name(self, name, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.get_escalation_chain_by_name...")

        if name is not None:
            query_filter = 'name:"{cn}"'.format(cn=name)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve escalation chain by name"
            resp = self.lm.rest_request(self.lm.GET, self.lm.ESCALATION_CHAINS_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_escalation_chains(self):
        self.lm.module.debug("Running EscalationChainUtils.get_alert_rules...")
        err_msg = "Failed to retrieve escalation chain"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.ESCALATION_CHAINS_BASE_URL, query_params=query_params,
                                    err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.send_create_request...")
        err_msg = "Failed to create escalation chain"
        return self.lm.rest_request(self.lm.POST, self.lm.ESCALATION_CHAINS_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.send_patch_request...")
        url = self.lm.ESCALATION_CHAINS_BASE_URL + "/" + str(id)
        err_msg = "Failed to update escalation chain"
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module)

    def send_delete_request(self, id, fail_module=True):
        self.lm.module.debug("Running EscalationChainUtils.send_delete_request...")
        url = self.lm.ESCALATION_CHAINS_BASE_URL + "/" + str(id)
        err_msg = "Failed to delete escalation chain " + str(id)
        self.lm.rest_request(self.lm.DELETE, url, err_msg=err_msg,
                             fail_module=fail_module)

class AlertRuleUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_alert_rule_id(self, id, name):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_id...")
        resp = self.get_alert_rule_info(id, name)
        if self.lm.success_response(resp):
            return resp[self.lm.ID]

    def get_alert_rule_info(self, id, name, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_info...")

        # try getting alert rule by ID
        resp = self.get_alert_rule_by_id(id, False)
        if not self.lm.success_response(resp) and name is not None:
            # try getting alert rule by name if unable to via ID
            resp = self.get_alert_rule_by_name(name, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Alert rule doesn't exist"
            else:
                err_msg = "Failed to retrieve alert rule \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_alert_rule_by_id(self, id, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_by_id...")
        err_msg = "Failed to retrieve alert rule id  '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.ALERT_RULE_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].startswith("The requestd alert rule does not exist"):
                resp = None
        return resp

    def get_alert_rule_by_name(self, name, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_by_name...")

        if name is not None:
            query_filter = 'name:"{cn}"'.format(cn=name)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve alert rule by name"
            resp = self.lm.rest_request(self.lm.GET, self.lm.ALERT_RULE_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_alert_rules(self):
        self.lm.module.debug("Running AlertRule.get_alert_rules...")
        err_msg = "Failed to retrieve alert rules"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.ALERT_RULE_BASE_URL, query_params=query_params, err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.send_create_request...")
        err_msg = "Failed to create Alert Rule"
        return self.lm.rest_request(self.lm.POST, self.lm.ALERT_RULE_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running AlertRule.send_patch_request...")
        url = self.lm.ALERT_RULE_BASE_URL + "/" + str(id)
        err_msg = "Failed to update alert rule"
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module)

    def send_delete_request(self, id, fail_module=True):
        self.lm.module.debug("Running AlertRule.send_delete_request...")
        err_msg = "Failed to delete alert rule " + str(id)
        self.lm.rest_request(self.lm.DELETE, self.lm.ALERT_RULE_BASE_URL + '/' + str(id), err_msg=err_msg,
                             fail_module=fail_module)

class RecipientUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_recipient_info(self, method, addr, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_info...")

        # try getting recipient by method and addr
        if method is not None and addr is not None:
            resp = self.get_recipient_by_method_and_addr(method, addr, False)
        elif addr is not None:
            resp = self.get_recipient_by_addr(addr, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Recipient doesn't exist"
            else:
                err_msg = "Failed to retrieve recipient \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_recipient_by_method_and_addr(self, method, addr, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_by_name...")

        if method is not None and addr is not None:
            query_filter = 'method:"{0}",addr:"{1}"'.format(method, addr)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve recipient by name and user"
            resp = self.lm.rest_request(self.lm.GET, self.lm.RECIPIENT_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

    def get_recipient_by_addr(self, addr, fail_module=True):
        self.lm.module.debug("Running AlertRuleUtils.get_alert_rule_by_name...")

        if addr is not None:
            query_filter = 'addr:"{0}"'.format(addr)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            err_msg = "Failed to retrieve recipient by name and user"
            resp = self.lm.rest_request(self.lm.GET, self.lm.RECIPIENT_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

class WebsiteCheckUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_website_check_info(self, id, name, fail_module=True):
        self.lm.module.debug("Running WebsiteCheckUtils.get_web_check_info...")

        resp = None
        if id is not None:
            resp = self.get_website_check_by_id(id, False)
        if not self.lm.success_response(resp) and name is not None:
            resp = self.get_website_check_by_name(name, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Web check doesn't exist "
            else:
                err_msg = "Failed to retrieve Web check \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_website_check_by_id(self, id, fail_module=True):
        self.lm.module.debug("Running WebsiteCheckUtils.get_web_check_by_id...")
        err_msg = "Failed to retrieve web check id  '" + str(id) + "'"

        resp = None
        if self.lm.valid_id(id):
            url = self.lm.WEBSITE_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].startswith("The requested web check does not exist"):
                resp = None
        return resp

    def get_website_check_by_name(self, name, fail_module=True):
        self.lm.module.debug("Running WebsiteCheckUtils.get_web_check_by_name...")
        err_msg = "Failed to retrieve web check name  '" + name + "'"

        if name is not None:
            query_filter = 'name:"{cn}"'.format(cn=name)
            query_params = {self.lm.FILTER: query_filter, self.lm.SORT: self.lm.ID}
            resp = self.lm.rest_request(self.lm.GET, self.lm.WEBSITE_BASE_URL, query_params=query_params,
                                        err_msg=err_msg, fail_module=fail_module)
            return self.lm.parse_filter_request_response(resp)

class OpsNoteUtils(object):
    def __init__(self, lm_obj):
        self.lm = lm_obj

    def get_ops_note_info(self, id, fail_module=True):
        self.lm.module.debug("Running OpsNoteUtils.get_ops_note_info...")

        resp = None
        if id is not None:
            resp = self.get_ops_note_by_id(id, False)
        if not self.lm.success_response(resp):
            if not resp:
                err_msg = "Ops note doesn't exist "
            else:
                err_msg = "Failed to retrieve Ops note \nResponse: " + str(resp)
            self.lm.handle_module_err(err_msg, fail_module)
        return resp

    def get_ops_note_by_id(self, id, fail_module=True):
        self.lm.module.debug("Running OpsNoteUtils.get_ops_note_by_id...")
        err_msg = "Failed to retrieve Ops note id  '" + str(id) + "'"

        resp = None
        if id is not None:
            url = self.lm.OPS_NOTE_BASE_URL + "/" + str(id)
            resp = self.lm.rest_request(self.lm.GET, url, err_msg=err_msg, fail_module=fail_module)
            if resp and not self.lm.success_response(resp) and resp[self.lm.ERROR_CODE] == 1404 \
                    and resp[self.lm.ERROR_MESSAGE].startswith("The requested ops note does not exist"):
                resp = None
        return resp

    def get_ops_notes(self):
        self.lm.module.debug("Running OpsNoteUtils.get_ops_notes...")
        err_msg = "Failed to retrieve Ops notes"
        query_params = {self.lm.SORT: self.lm.ID, self.lm.SIZE: self.lm.size}
        return self.lm.paginated_request(self.lm.OPS_NOTE_BASE_URL, query_params=query_params, err_msg=err_msg)

    def send_create_request(self, data, fail_module=True):
        self.lm.module.debug("Running OpsNoteUtils.send_create_request...")
        err_msg = "Failed to create Ops note"
        return self.lm.rest_request(self.lm.POST, self.lm.OPS_NOTE_BASE_URL, data, err_msg=err_msg,
                                    fail_module=fail_module)

    def send_patch_request(self, id, data, fail_module=True):
        self.lm.module.debug("Running OpsNoteUtils.send_patch_request...")
        url = self.lm.OPS_NOTE_BASE_URL + "/" + str(id)
        err_msg = "Failed to update ops note"
        return self.lm.rest_request(self.lm.PATCH, url, data, err_msg=err_msg, fail_module=fail_module)

    def send_delete_request(self, id, fail_module=True):
        self.lm.module.debug("Running OpsNoteUtils.send_delete_request...")
        err_msg = "Failed to delete ops note " + str(id)
        self.lm.rest_request(self.lm.DELETE, self.lm.OPS_NOTE_BASE_URL + '/' + str(id), err_msg=err_msg,
                             fail_module=fail_module)
        
