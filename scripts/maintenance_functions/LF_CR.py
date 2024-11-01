from time import time

"""Execution of the LF_CR function
Properties:
    Method: 1 - Fact table load
    Target table: catalog_returns
"""

def create_view(connection):
    print('\tCreating view crv')
    query = '''CREATE VIEW crv as
SELECT
	d_date_sk cr_returned_date_sk,
	t_time_sk cr_returned_time_sk,
	i_item_sk cr_item_sk,
	c1.c_customer_sk cr_refunded_customer_sk,
	c1.c_current_cdemo_sk cr_refunded_cdemo_sk,
	c1.c_current_hdemo_sk cr_refunded_hdemo_sk,
	c1.c_current_addr_sk cr_refunded_addr_sk,
	c2.c_customer_sk cr_returning_customer_sk,
	c2.c_current_cdemo_sk cr_returning_cdemo_sk,
	c2.c_current_hdemo_sk cr_returning_hdemo_sk,
	c2.c_current_addr_sk cr_returing_addr_sk,
	cc_call_center_sk cr_call_center_sk,
	cp_catalog_page_sk CR_CATALOG_PAGE_SK,
	sm_ship_mode_sk CR_SHIP_MODE_SK,
	w_warehouse_sk CR_WAREHOUSE_SK,
	r_reason_sk cr_reason_sk,
	cret_order_id cr_order_number,
	cret_return_qty cr_return_quantity,
	cret_return_amt cr_return_amt,
	cret_return_tax cr_return_tax,
	cret_return_amt + cret_return_tax AS cr_return_amt_inc_tax,
	cret_return_fee cr_fee,
	cret_return_ship_cost cr_return_ship_cost,
	cret_refunded_cash cr_refunded_cash,
	cret_reversed_charge cr_reversed_charge,
	cret_merchant_credit cr_merchant_credit,
	cret_return_amt + cret_return_tax + cret_return_fee - cret_refunded_cash - cret_reversed_charge - cret_merchant_credit cr_net_loss
FROM
	s_catalog_returns
	LEFT OUTER JOIN date_dim ON (cast(cret_return_date as date) = d_date)
	LEFT OUTER JOIN time_dim ON (
		(
			CAST(substr(cret_return_time, 1, 2) AS integer) * 3600 + CAST(substr(cret_return_time, 4, 2) AS integer) * 60 + CAST(substr(cret_return_time, 7, 2) AS integer)
		) = t_time
	)
	LEFT OUTER JOIN item ON (cret_item_id = i_item_id)
	LEFT OUTER JOIN customer c1 ON (cret_return_customer_id = c1.c_customer_id)
	LEFT OUTER JOIN customer c2 ON (cret_refund_customer_id = c2.c_customer_id)
	LEFT OUTER JOIN reason ON (cret_reason_id = r_reason_id)
	LEFT OUTER JOIN call_center ON (cret_call_center_id = cc_call_center_id)
	LEFT OUTER JOIN catalog_page ON (cret_catalog_page_id = cp_catalog_page_id)
	LEFT OUTER JOIN ship_mode ON (cret_shipmode_id = sm_ship_mode_id)
	LEFT OUTER JOIN warehouse ON (cret_warehouse_id = w_warehouse_id)
WHERE
	i_rec_end_date IS NULL
	AND cc_rec_end_date IS NULL;'''

    connection.sql(query)

def insert_from_view(connection):
    query = 'INSERT OR IGNORE INTO catalog_returns SELECT DISTINCT(*) FROM crv'
    print(f'\tQuery: {query}')
    connection.sql(query)

def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function LF_CR, test #{test}, run #{run}, stream #{stream}')
    start_time = time()
    create_view(connection)
    insert_from_view(connection)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time