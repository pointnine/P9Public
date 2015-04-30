# Circle API
# Copyright (c) 2012-2020, Point Nine Limited
# All rights reserved.
#
# info@p9ft.com
# http://www.p9ft.com/terms.html
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Point Nine Limited or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# POINT NINE LIMITED AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL POINT NINE LIMITED OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------
import json
from sys import version_info

PYTHON_3 = version_info >= (3, 0)
if PYTHON_3:
    from urllib import request as urllib2
else:
    import urllib2


class RPCClient(object):
    """ Allows accessing rpc workflows from Python
    """
    PROTOCOL = 'https'
    REALM = 'Platforma Login'
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self):
        self.opener = None

    def compose_url(self, workflow, action):
        raise NotImplementedError

    def run_raw(self, workflow, action, **kwargs):
        """ runs a request, returns a response
        """
        URL = self.compose_url(workflow, action)
        data = json.dumps(kwargs)
        request = urllib2.Request(URL,
            data=data.encode('ascii') if PYTHON_3 else data,
            headers=self.HEADERS)
        result = self.opener.open(request).read()
        return result.decode('ascii') if PYTHON_3 else result

    def run_json(self, workflow, action, **kwargs):
        """ runs a request, returns parsed response, in case it's json
        """
        return json.loads(self.run_raw(workflow, action, **kwargs))

    def run(self, workflow, action, **kwargs):
        """ runs a request, returns parsed json 'data' value
            assuming response was good
        """
        return self.run_json(workflow, action, **kwargs)['data']

    def compose_error_message(self, messages):
        raise NotImplementedError

    def parse_response(self, response):
        """ reads the response assuming it's ModelRowResult
            or raises an exception if request failed
        """
        if response["status"] == "ok":
            return response["data"][0]['rows']
        messages = [error["message"] for error in response["errors"]]
        raise Exception(self.compose_error_message(messages))


class CircleClient(RPCClient):
    """ Allows accessing circle workflows from Python
    """
    def __init__(self, host, fund, username, password):
        self.HOST = host
        self.FUND = fund
        pwd_mgr = urllib2.HTTPPasswordMgr()
        pwd_mgr.add_password(self.REALM, self.HOST, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr=pwd_mgr)
        self.opener = urllib2.build_opener(handler)

    def compose_url(self, workflow, action):
        url = "%s://%s/%s/do/%s/%s/" % (
            self.PROTOCOL, self.HOST, self.FUND, workflow, action)
        return url

    def compose_error_message(self, messages):
        return "Circle reports error: " + "\n".join(messages)


class QueueClient(RPCClient):
    """ Allows accessing queue workflows from Python
    """
    def __init__(self, host, fund, api_key):
        self.HOST = host
        self.FUND = fund
        self.API_KEY = api_key
        self.opener = urllib2.build_opener()

    def run_raw(self, workflow, action, **kwargs):
        """ runs a request, returns a response
        """
        kwargs["__api_key"] = self.API_KEY
        return super(QueueClient, self).run_raw(workflow, action, **kwargs)

    def compose_url(self, workflow, action):
        url = "%s://%s/%s/_%s/%s/" % (
            self.PROTOCOL, self.HOST, self.FUND, workflow, action)
        return url

    def compose_error_message(self, messages):
        return "Queue reports error: " + "\n".join(messages)




def demo():
    cc = CircleClient(host='circle.p9ft.com', fund='areski',
                      username='rpcclient', password='rpcdemorpcqph')
#    cc = CircleClient(host='localhost', fund='test',
#        username='guest', password='demodemodemo');cc.PROTOCOL = 'http'

    response = cc.run('PyClientCalendarWorkflow', 'get_calendar')
    print(response)
    #dict of properties

    print(cc.run('PyClientCalendarWorkflow', 'get_year_start',
                 date='2012-04-07'))
    #2012-01-02
    print(cc.run('PyClientCalendarWorkflow', 'get_month_start',
                 date='2012-04-07'))
    #2012-04-02
    print(cc.run('PyClientCalendarWorkflow', 'get_business_day',
                 date='2012-04-07', next=True))
    #2012-04-10
    print(cc.run('PyClientCalendarWorkflow', 'get_business_day',
                 date='2012-04-07', next=False))
    #2012-04-05

    print(cc.run('PyClientCalendarWorkflow', 'is_holiday', date='2012-04-07'))
    #True
    print(cc.run('PyClientCalendarWorkflow', 'is_holiday', date='2012-04-05'))
    #False

    print(cc.run('PyClientCalendarWorkflow', 'offset', date='2012-04-07',
                 count=10))
    #2012-04-23

    print(cc.run('PyClientCalendarWorkflow', 'offset',
                 date='2012-04-07', count=-10))
    #2012-03-23

    print(cc.run('PyClientCalendarWorkflow', 'working_days_diff',
                 date1='2012-04-07', date2='2012-04-12'))
    #3

    print(cc.run('PyClientCalendarWorkflow', 'working_days',
                 date1='2012-04-07', date2='2012-04-15'))
    #[u'2012-04-10', u'2012-04-11', u'2012-04-12', u'2012-04-13']

    response = cc.run_json('UISettingsWorkflow', 'get_settings')
    data = response['data']
    for key in data.keys():
        if 'CALENDAR' in key:
            print('%s = %s' % (key, data[key]))
    #result:
    #CALENDAR_PREVIOUS_DAY = 2013-03-13
    #CALENDAR_YEAR_END = 2013-12-31
    #CALENDAR_MONTH_START = 2013-03-01
    #CALENDAR_PNL_YTD_FROM = 2012-12-31
    #CALENDAR_TODAY = 2013-03-14
    #CALENDAR_PNL_MTD_FROM = 2013-02-28
    #CALENDAR_BUSINESS_DAY = 2013-03-14
    #CALENDAR_YEAR_START = 2013-01-02

    print(cc.run_json('PyClientDataModelWorkflow', 'get_model_description',
                      model_name='UnknownModel'))
    print(cc.run_raw('PyClientDataModelWorkflow', 'get_model_description',
                     model_name='PositionReportModel'))

    print(cc.run('UIPositionReportQueryWorkflow', 'get_standard',
                 AsOfDate='2013-03-13', KnowledgeDate='2013-03-13',
                 IncludeNonTrading='N', IncludeTrading='Y'))
    # gives whole position report

def test_trade_upload():
    """ Allows uploading trades to the Circle system
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: client.py path_to_file")
        return
    payload = open(sys.argv[1], 'r').read()
    cc = CircleClient(host='circle.p9ft.com', fund='areski',
        username='rpcclient', password='rpcdemorpcqph')
    response = cc.run_json('UIGridWorkflow', 'process', payload = payload, notify = True)
    print(response)

def test_trade_upload_to_queue():
    """ Allows uploading trades to the Queue
    """
    import sys
    if len(sys.argv) < 2:
        print("Usage: client.py path_to_file")
        return
    payload = open(sys.argv[1], 'r').read()

    #replace sample api_key below with real one
    cc = QueueClient(host='circle.p9ft.com', fund='apps', api_key='11111111-1111-1111-1111-111111111111')

    response = cc.run_json('areski', 'load_trades', payload = payload)
    print(response)

def test_positions_upload():
    """ Allows uploading positions to the Circle system
    """
    import sys
    # if len(sys.argv) < 2:
    #     print("Usage: client.py path_to_file")
    #     return
    # payload = open(sys.argv[1], 'r').read()
    payload = """{
    "date": "2014-03-07",
    "trades": {
            "E10.2": {
            "FX": 0.7207207207207208,
            "Forward": 3126.46,
            "Funding": 73.3530048663213,
            "PV": 0.0,
            "PnL": 136574.11550486615,
            "Size": 90.0,
            "Spot": 3126.46
            }
    }}"""

    cc = CircleClient(host='circle.p9ft.com', fund='areski',
        username='rpcclient', password='rpcdemorpcqph')
    response = cc.run_json('UIGridWorkflow', 'load_positions', payload = payload, notify = True)
    print(response)

def test_positions_upload_to_queue():
    """ Allows uploading positions to the Queue
    """
    import sys
    # if len(sys.argv) < 2:
    #     print("Usage: client.py path_to_file")
    #     return
    # payload = open(sys.argv[1], 'r').read()
    payload = """{
    "date": "2014-03-07",
    "trades": {
            "E10.2": {
            "FX": 0.7207207207207208,
            "Forward": 3126.46,
            "Funding": 73.3530048663213,
            "PV": 0.0,
            "PnL": 136574.11550486615,
            "Size": 90.0,
            "Spot": 3126.46
            }
    }}"""

    #replace sample api_key below with real one
    cc = QueueClient(host='circle.p9ft.com', fund='apps', api_key='11111111-1111-1111-1111-111111111111')

    response = cc.run_json('areski', 'load_positions', payload = payload)
    print(response)



if __name__ == '__main__':
    #demo()  # uncomment this to run demo
    #test_positions_upload()
    #test_trade_upload_to_queue()
    test_positions_upload_to_queue()
    pass
