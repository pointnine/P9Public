import urllib2
import json

class CircleClient:
    """ Allows accessing circle workflows from Python
    """
    PROTOCOL = 'https'
    REALM    = 'Platforma Login'
    HEADERS  = {'Content-Type' : 'application/json' }

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
        URL = "%s://%s/%s/do/%s/%s/" % (self.PROTOCOL, self.HOST, self.FUND, workflow, action)
        data = json.dumps(kwargs)
        request = urllib2.Request(URL, data=data, headers=self.HEADERS)
        str = self.opener.open(request).read()
        return str

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
    cc = CircleClient(host='circle.p9ft.com', fund='demo', username='guest', password='demodemodemo')
    #cc = CircleClient(host='localhost', fund='test', username='guest', password='demodemodemo');cc.PROTOCOL = 'http'

    response = cc.run('PyClientCalendarWorkflow', 'get_calendar')
    print response
    #dict of properties

    print cc.run('PyClientCalendarWorkflow', 'get_year_start', date='2012-04-07')
    #2012-01-02
    print cc.run('PyClientCalendarWorkflow', 'get_month_start', date='2012-04-07')
    #2012-04-02
    print cc.run('PyClientCalendarWorkflow', 'get_business_day', date='2012-04-07', next=True)
    #2012-04-10
    print cc.run('PyClientCalendarWorkflow', 'get_business_day', date='2012-04-07', next=False)
    #2012-04-05

    print cc.run('PyClientCalendarWorkflow', 'is_holiday', date='2012-04-07')
    #True
    print cc.run('PyClientCalendarWorkflow', 'is_holiday', date='2012-04-05')
    #False

    print cc.run('PyClientCalendarWorkflow', 'offset', date='2012-04-07', count=10)
    #2012-04-23

    print cc.run('PyClientCalendarWorkflow', 'offset', date='2012-04-07', count=-10)
    #2012-03-23

    print cc.run('PyClientCalendarWorkflow', 'working_days_diff', date1='2012-04-07', date2='2012-04-12')
    #3

    print cc.run('PyClientCalendarWorkflow', 'working_days', date1='2012-04-07', date2='2012-04-15')
    #[u'2012-04-10', u'2012-04-11', u'2012-04-12', u'2012-04-13']

    response = cc.run_json('UISettingsWorkflow', 'get_settings')
    data = response['data']
    for key in data.keys():
        if 'CALENDAR' in key:
            print key, '=', data[key]
    #result:
    #CALENDAR_PREVIOUS_DAY = 2013-03-13
    #CALENDAR_YEAR_END = 2013-12-31
    #CALENDAR_MONTH_START = 2013-03-01
    #CALENDAR_PNL_YTD_FROM = 2012-12-31
    #CALENDAR_TODAY = 2013-03-14
    #CALENDAR_PNL_MTD_FROM = 2013-02-28
    #CALENDAR_BUSINESS_DAY = 2013-03-14
    #CALENDAR_YEAR_START = 2013-01-02


    print cc.run_json('PyClientDataModelWorkflow', 'get_model_description', model_name='UnknownModel')
    print cc.run_raw('PyClientDataModelWorkflow', 'get_model_description', model_name='PositionReportModel')

    print cc.run('UIPositionReportQueryWorkflow', 'get_standard',
        AsOfDate='2013-03-13', KnowledgeDate='2013-03-13', IncludeNonTrading='N', IncludeTrading='Y', page=1, start=0, limit=1000)
    # gives whole position report

if __name__ == '__main__':
    #demo() # uncomment this to run demo
    pass
