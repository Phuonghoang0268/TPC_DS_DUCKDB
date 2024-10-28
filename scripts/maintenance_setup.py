import os

def create_tables(connection):
    print('\nCreating tables for maintenance test')
    query = '''-- ============================================================
--   Table: s_purchase_lineitem                                
-- ============================================================
create table s_purchase_lineitem
(
    plin_purchase_id            integer               not null,
    plin_line_number            integer               not null,
    plin_item_id                char(16)                      ,
    plin_promotion_id           char(16)                      ,
    plin_quantity               integer                       ,
    plin_sale_price             numeric(7,2)                  ,
    plin_coupon_amt             numeric(7,2)                  ,
    plin_comment                varchar(100)                  
);

-- ============================================================
--   Table: s_purchase                                         
-- ============================================================
create table s_purchase
(
    purc_purchase_id            integer               not null,
    purc_store_id               char(16)                      ,
    purc_customer_id            char(16)                      ,
    purc_purchase_date          char(10)                      ,
    purc_purchase_time          integer                       ,
    purc_register_id            integer                       ,
    purc_clerk_id               integer                       ,
    purc_comment                char(100)                     
);

-- ============================================================
--   Table: s_catalog_order                                    
-- ============================================================
create table s_catalog_order
(
    cord_order_id               integer               not null,
    cord_bill_customer_id       char(16)                      ,
    cord_ship_customer_id       char(16)                      ,
    cord_order_date             char(10)                      ,
    cord_order_time             integer                       ,
    cord_ship_mode_id           char(16)                      ,
    cord_call_center_id         char(16)                      ,
    cord_order_comments         varchar(100)                  
);

-- ============================================================
--   Table: s_web_order                                        
-- ============================================================
create table s_web_order
(
    word_order_id               integer               not null,
    word_bill_customer_id       char(16)                      ,
    word_ship_customer_id       char(16)                      ,
    word_order_date             char(10)                      ,
    word_order_time             integer                       ,
    word_ship_mode_id           char(16)                      ,
    word_web_site_id            char(16)                      ,
    word_order_comments         char(100)                     
);

-- ============================================================
--   Table: s_catalog_order_lineitem                           
-- ============================================================
create table s_catalog_order_lineitem
(
    clin_order_id               integer               not null,
    clin_line_number            integer               not null,
    clin_item_id                char(16)                      ,
    clin_promotion_id           char(16)                      ,
    clin_quantity               integer                       ,
    clin_sales_price            numeric(7,2)                  ,
    clin_coupon_amt             numeric(7,2)                  ,
    clin_warehouse_id           char(16)                      ,
    clin_ship_date              char(10)                      ,
    clin_catalog_number         integer                       ,
    clin_catalog_page_number    integer                       ,
    clin_ship_cost              numeric(7,2)                  
);

-- ============================================================
--   Table: s_web_order_lineitem                               
-- ============================================================
create table s_web_order_lineitem
(
    wlin_order_id               integer               not null,
    wlin_line_number            integer               not null,
    wlin_item_id                char(16)                      ,
    wlin_promotion_id           char(16)                      ,
    wlin_quantity               integer                       ,
    wlin_sales_price            numeric(7,2)                  ,
    wlin_coupon_amt             numeric(7,2)                  ,
    wlin_warehouse_id           char(16)                      ,
    wlin_ship_date              char(10)                      ,
    wlin_ship_cost              numeric(7,2)                  ,
    wlin_web_page_id            char(16)                      
);

-- ============================================================
--   Table: s_store_returns                                    
-- ============================================================
create table s_store_returns
(
    sret_store_id               char(16)                      ,
    sret_purchase_id            char(16)              not null,
    sret_line_number            integer               not null,
    sret_item_id                char(16)              not null,
    sret_customer_id            char(16)                      ,
    sret_return_date            char(10)                      ,
    sret_return_time            char(10)                      ,
    sret_ticket_number          char(20)                      ,
    sret_return_qty             integer                       ,
    sret_return_amt             numeric(7,2)                  ,
    sret_return_tax             numeric(7,2)                  ,
    sret_return_fee             numeric(7,2)                  ,
    sret_return_ship_cost       numeric(7,2)                  ,
    sret_refunded_cash          numeric(7,2)                  ,
    sret_reversed_charge        numeric(7,2)                  ,
    sret_store_credit           numeric(7,2)                  ,
    sret_reason_id              char(16)                      
);

-- ============================================================
--   Table: s_catalog_returns                                  
-- ============================================================
create table s_catalog_returns
(
    cret_call_center_id         char(16)                      ,
    cret_order_id               integer               not null,
    cret_line_number            integer               not null,
    cret_item_id                char(16)              not null,
    cret_return_customer_id     char(16)                      ,
    cret_refund_customer_id     char(16)                      ,
    cret_return_date            char(10)                      ,
    cret_return_time            char(10)                      ,
    cret_return_qty             integer                       ,
    cret_return_amt             numeric(7,2)                  ,
    cret_return_tax             numeric(7,2)                  ,
    cret_return_fee             numeric(7,2)                  ,
    cret_return_ship_cost       numeric(7,2)                  ,
    cret_refunded_cash          numeric(7,2)                  ,
    cret_reversed_charge        numeric(7,2)                  ,
    cret_merchant_credit        numeric(7,2)                  ,
    cret_reason_id              char(16)                      ,
    cret_shipmode_id            char(16)                      ,
    cret_catalog_page_id        char(16)                      ,
    cret_warehouse_id           char(16)                      
);

-- ============================================================
--   Table: s_web_returns                                      
-- ============================================================
create table s_web_returns
(
    wret_web_page_id            char(16)                      ,
    wret_order_id               integer               not null,
    wret_line_number            integer               not null,
    wret_item_id                char(16)              not null,
    wret_return_customer_id     char(16)                      ,
    wret_refund_customer_id     char(16)                      ,
    wret_return_date            char(10)                      ,
    wret_return_time            char(10)                      ,
    wret_return_qty             integer                       ,
    wret_return_amt             numeric(7,2)                  ,
    wret_return_tax             numeric(7,2)                  ,
    wret_return_fee             numeric(7,2)                  ,
    wret_return_ship_cost       numeric(7,2)                  ,
    wret_refunded_cash          numeric(7,2)                  ,
    wret_reversed_charge        numeric(7,2)                  ,
    wret_account_credit         numeric(7,2)                  ,
    wret_reason_id              char(16)                      
);

-- ============================================================
--   Table: s_inventory                                        
-- ============================================================
create table s_inventory
(
    invn_warehouse_id           char(16)              not null,
    invn_item_id                char(16)              not null,
    invn_date                   char(10)              not null,
    invn_qty_on_hand            integer                       
);
'''
    connection.sql(query)

def load_data(scale, test, run, connection):
    print('\nLoading data into tables for maintenance test')
    print(f'Scale: {scale}, test: {test}, run: {run}')
    stream = (test - 1) * 2 + (run - 1) + 1
    flatfile_dir = f'../refresh_data/scale_{scale}/stream_{stream}/'
    tables = ['s_catalog_order',
              's_catalog_order_lineitem',
              's_catalog_returns',
              's_inventory',
              's_purchase',
              's_purchase_lineitem',
              's_store_returns',
              's_web_order',
              's_web_order_lineitem',
              's_web_returns']
    for table in tables:
        print(f'\n\tDeleting all existing rows in {table}')
        connection.sql(f'DELETE FROM {table}')
        file = f'{table}_{stream}.dat'
        query = f"COPY {table} FROM '{flatfile_dir + file}' (DELIMETER '|')"
        print(f'\tExecuting: {query}')
        connection.sql(query)
    return True

def clear_views(connection):
    print('\nDropping views if exist')
    views = ['crv', 'csv', 'iv', 'srv', 'ssv', 'wrv', 'wsv']
    for view in views:
        print(f'\tDropping view {view}')
        connection.sql(f'DROP VIEW IF EXISTS {view}')