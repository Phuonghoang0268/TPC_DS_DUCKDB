select  *
from (select avg(ss_list_price) B1_LP
            ,count(ss_list_price) B1_CNT
            ,count(distinct ss_list_price) B1_CNTD
      from store_sales
      where ss_quantity between 0 and 5
        and (ss_list_price between 125 and 125+10 
             or ss_coupon_amt between 10280 and 10280+1000
             or ss_wholesale_cost between 65 and 65+20)) B1,
     (select avg(ss_list_price) B2_LP
            ,count(ss_list_price) B2_CNT
            ,count(distinct ss_list_price) B2_CNTD
      from store_sales
      where ss_quantity between 6 and 10
        and (ss_list_price between 81 and 81+10
          or ss_coupon_amt between 10959 and 10959+1000
          or ss_wholesale_cost between 5 and 5+20)) B2,
     (select avg(ss_list_price) B3_LP
            ,count(ss_list_price) B3_CNT
            ,count(distinct ss_list_price) B3_CNTD
      from store_sales
      where ss_quantity between 11 and 15
        and (ss_list_price between 66 and 66+10
          or ss_coupon_amt between 4390 and 4390+1000
          or ss_wholesale_cost between 31 and 31+20)) B3,
     (select avg(ss_list_price) B4_LP
            ,count(ss_list_price) B4_CNT
            ,count(distinct ss_list_price) B4_CNTD
      from store_sales
      where ss_quantity between 16 and 20
        and (ss_list_price between 169 and 169+10
          or ss_coupon_amt between 1201 and 1201+1000
          or ss_wholesale_cost between 33 and 33+20)) B4,
     (select avg(ss_list_price) B5_LP
            ,count(ss_list_price) B5_CNT
            ,count(distinct ss_list_price) B5_CNTD
      from store_sales
      where ss_quantity between 21 and 25
        and (ss_list_price between 67 and 67+10
          or ss_coupon_amt between 3282 and 3282+1000
          or ss_wholesale_cost between 76 and 76+20)) B5,
     (select avg(ss_list_price) B6_LP
            ,count(ss_list_price) B6_CNT
            ,count(distinct ss_list_price) B6_CNTD
      from store_sales
      where ss_quantity between 26 and 30
        and (ss_list_price between 8 and 8+10
          or ss_coupon_amt between 14933 and 14933+1000
          or ss_wholesale_cost between 44 and 44+20)) B6
limit 100;