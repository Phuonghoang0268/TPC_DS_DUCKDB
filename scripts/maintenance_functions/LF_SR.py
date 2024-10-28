from time import time

"""Execution of the LF_SR function
Properties:
    Method: 1 - Fact table load
    Target table: store_returns
"""

def create_view(connection):
    print('\tCreating view srv')
    query = '''CREATE view srv as
SELECT
	d_date_sk sr_returned_date_sk,
	t_time_sk sr_return_time_sk,
	i_item_sk sr_item_sk,
	c_customer_sk sr_customer_sk,
	c_current_cdemo_sk sr_cdemo_sk,
	c_current_hdemo_sk sr_hdemo_sk,
	c_current_addr_sk sr_addr_sk,
	s_store_sk sr_store_sk,
	r_reason_sk sr_reason_sk,
	sret_ticket_number sr_ticket_number,
	sret_return_qty sr_return_quantity,
	sret_return_amt sr_return_amt,
	sret_return_tax sr_return_tax,
	sret_return_amt + sret_return_tax sr_return_amt_inc_tax,
	sret_return_fee sr_fee,
	sret_return_ship_cost sr_return_ship_cost,
	sret_refunded_cash sr_refunded_cash,
	sret_reversed_charge sr_reversed_charge,
	sret_store_credit sr_store_credit,
	sret_return_amt + sret_return_tax + sret_return_fee - sret_refunded_cash - sret_reversed_charge - sret_store_credit sr_net_loss
FROM
	s_store_returns
	LEFT OUTER JOIN date_dim ON (cast(sret_return_date as date) = d_date)
	LEFT OUTER JOIN time_dim ON (
		(
			cast(substr(sret_return_time, 1, 2) AS integer) * 3600 + cast(substr(sret_return_time, 4, 2) AS integer) * 60 + cast(substr(sret_return_time, 7, 2) AS integer)
		) = t_time
	)
	LEFT OUTER JOIN item ON (sret_item_id = i_item_id)
	LEFT OUTER JOIN customer ON (sret_customer_id = c_customer_id)
	LEFT OUTER JOIN store ON (sret_store_id = s_store_id)
	LEFT OUTER JOIN reason ON (sret_reason_id = r_reason_id)
WHERE
	i_rec_end_date IS NULL
	AND s_rec_end_date IS NULL;'''

    connection.sql(query)

def insert_from_view(connection):
    query = 'INSERT OR IGNORE INTO store_returns SELECT DISTINCT(*) FROM srv'
    print(f'\tQuery: {query}')
    connection.sql(query)

def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function LF_SR, test #{test}, run #{run}, stream #{stream}')
    start_time = time()
    create_view(connection)
    insert_from_view(connection)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time