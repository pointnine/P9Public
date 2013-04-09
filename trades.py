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

def get_trades(cc, FromDate, ToDate, FilterText=None):
	return cc.run_raw('UITransactionActivityQueryWorkflow', 'get_transactions_simple',
		FromDate=FromDate,ToDate=ToDate, FilterText=FilterText)

def get_forwards(cc, **kwargs):
	return get_trades(cc, FilterText="Forward", **kwargs)

def get_futures(cc, **kwargs):
	return get_trades(cc, FilterText="Future", **kwargs)


def demo_trades():
	cc = CircleClient(host='circle.p9ft.com', fund='areski',
	                  username='rpcclient', password='rpcdemorpcqph')

	print(get_trades(	cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))
	print(get_futures(	cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))
	print(get_forwards(	cc, FromDate = '2011-11-10', ToDate = '2011-11-25'))


if __name__ == '__main__':
    demo_trades()  

