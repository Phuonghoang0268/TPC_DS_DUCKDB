from time import time

"""Execution of the LF_SS function
Properties:
    Method: 1 - Fact table load
    Target table: store_sales
"""

def create_view(connection):
    print('\tCreating view ssv')
    query = '''CREATE view ssv as
SELECT
	d_date_sk ss_sold_date_sk,
	t_time_sk ss_sold_time_sk,
	i_item_sk ss_item_sk,
	c_customer_sk ss_customer_sk,
	c_current_cdemo_sk ss_cdemo_sk,
	c_current_hdemo_sk ss_hdemo_sk,
	c_current_addr_sk ss_addr_sk,
	s_store_sk ss_store_sk,
	p_promo_sk ss_promo_sk,
	purc_purchase_id ss_ticket_number,
	plin_quantity ss_quantity,
	i_wholesale_cost ss_wholesale_cost,
	i_current_price ss_list_price,
	plin_sale_price ss_sales_price,
	(i_current_price - plin_sale_price) * plin_quantity ss_ext_discount_amt,
	plin_sale_price * plin_quantity ss_ext_sales_price,
	i_wholesale_cost * plin_quantity ss_ext_wholesale_cost,
	i_current_price * plin_quantity ss_ext_list_price,
	i_current_price * s_tax_precentage ss_ext_tax,
	plin_coupon_amt ss_coupon_amt,
	(plin_sale_price * plin_quantity) - plin_coupon_amt ss_net_paid,
	(
		(plin_sale_price * plin_quantity) - plin_coupon_amt
	) *(1 + s_tax_precentage) ss_net_paid_inc_tax,
	(
		(plin_sale_price * plin_quantity) - plin_coupon_amt
	) -(plin_quantity * i_wholesale_cost) ss_net_profit
FROM
	s_purchase
	LEFT OUTER JOIN customer ON (purc_customer_id = c_customer_id)
	LEFT OUTER JOIN store ON (purc_store_id = s_store_id)
	LEFT OUTER JOIN date_dim ON (cast(purc_purchase_date as date) = d_date)
	LEFT OUTER JOIN time_dim ON (PURC_PURCHASE_TIME = t_time)
	JOIN s_purchase_lineitem ON (purc_purchase_id = plin_purchase_id)
	LEFT OUTER JOIN promotion ON plin_promotion_id = p_promo_id
	LEFT OUTER JOIN item ON plin_item_id = i_item_id
WHERE
	purc_purchase_id = plin_purchase_id
	AND i_rec_end_date is NULL
	AND s_rec_end_date is NULL;'''

    connection.sql(query)

def insert_from_view(connection):
    query = 'INSERT OR IGNORE INTO store_sales SELECT DISTINCT(*) FROM ssv'
    print(f'\tQuery: {query}')
    connection.sql(query)

def execute(scale, test, run, connection):
    stream = (test - 1) * 2 + (run - 1) + 1
    print(f'\nExecuting function LF_SS, test #{test}, run #{run}, stream #{stream}')
    start_time = time()
    create_view(connection)
    insert_from_view(connection)
    end_time = time()
    print(f'\n\tExecution time: {end_time - start_time} seconds')
    return end_time - start_time