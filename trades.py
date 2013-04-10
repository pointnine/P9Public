# Circle API
#
# Trade blotter
#
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
from client import CircleClient

def get_trades(cc, FromDate="1950-01-01", ToDate="9999-12-31", FilterText=None, limit=20):
    response = cc.run_json('UITransactionActivityQueryWorkflow', 'get_transactions_simple',
        FromDate=FromDate,ToDate=ToDate, FilterText=FilterText, page=1, start=0, limit=limit)
    return cc.parse_response(response)

def get_forwards(cc, **kwargs):
    return get_trades(cc, FilterText="Forward", **kwargs)

def get_futures(cc, **kwargs):
    return get_trades(cc, FilterText="Future", **kwargs)

def update_trade(cc, trade):
    response = cc.run_json('UITransactionActivityQueryWorkflow', 'update_transaction', row_data=trade)
    return cc.parse_response(response)

def short_info(trade):
    return ("P9TradeId=%(P9TradeId)s\n"
            "P9Ticker='%(P9Ticker)s'\n"
            "Instr=%(UnderlyingDeliveryDirection)s %(Quantity)g '%(UnderlyingInstrument)s' CleanPrice=%(CleanPrice).2f\n"
            "Settl=%(SettlementDeliveryDirection)s %(SettlementAmount)g %(SettlementCurrency)s\n"
            % trade)

def print_trades(trades):
    for trade in trades:
        print(short_info(trade))

#------------------------------------------------------------------------------------------------------------
# Examples
#------------------------------------------------------------------------------------------------------------

def demo_trades(cc):
    print_trades(get_trades(    cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))
    print_trades(get_futures(   cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))
    print_trades(get_forwards(  cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))

def demo_edit(cc):
    trades = get_trades(cc, FromDate = '2011-11-10', ToDate = '2011-11-25', limit=1, FilterText="Futures")
    trade = trades[0]
    print(short_info(trade))
    trade['CleanPrice'] = 22  # Update CleanPrice
    update_trade(cc, trade)
    print('Trade has been updated')

def demo_edit2(cc):
    spot_trade = get_trades(cc, FilterText="Spot", limit=1)[0]
    print(short_info(spot_trade))
    spot_trade['SettlementAmount'] = 400000  # Update SettlementAmount
    update_trade(cc, spot_trade)
    print('Trade has been updated')


def demo():
    cc = CircleClient(host='circle.p9ft.com', fund='areski',
                      username='rpcclient', password='rpcdemorpcqph')

    demo_trades(cc)
    demo_edit(cc)
    demo_edit2(cc)

if __name__ == '__main__':
    demo()
