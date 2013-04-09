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


class CircleClient(object):
    """ Allows accessing circle workflows from Python
    """
    PROTOCOL = 'https'
    REALM = 'Platforma Login'
    HEADERS = {'Content-Type': 'application/json'}

    def __init__(self, host, fund, username, password):
        self.HOST = host
        self.FUND = fund
        pwd_mgr = urllib2.HTTPPasswordMgr()
        pwd_mgr.add_password(self.REALM, self.HOST, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr=pwd_mgr)
        self.opener = urllib2.build_opener(handler)

    def run_raw(self, workflow, action, **kwargs):
        """ runs a request, returns a response
        """
        URL = "%s://%s/%s/do/%s/%s/" % (
            self.PROTOCOL, self.HOST, self.FUND, workflow, action)
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

if __name__ == '__main__':
    demo()  # uncomment this to run demo
    pass
