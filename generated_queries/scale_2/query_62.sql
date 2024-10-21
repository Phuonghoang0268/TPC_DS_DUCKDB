select  distinct(i_product_name)
 from item i1
 where i_manufact_id between 991 and 991+40 
   and (select count(*) as item_cnt
        from item
        where (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'ivory' or i_color = 'misty') and 
        (i_units = 'Oz' or i_units = 'Box') and
        (i_size = 'medium' or i_size = 'large')
        ) or
        (i_category = 'Women' and
        (i_color = 'sandy' or i_color = 'pale') and
        (i_units = 'Gross' or i_units = 'Pound') and
        (i_size = 'economy' or i_size = 'extra large')
        ) or
        (i_category = 'Men' and
        (i_color = 'purple' or i_color = 'grey') and
        (i_units = 'Bunch' or i_units = 'Carton') and
        (i_size = 'N/A' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'cream' or i_color = 'mint') and
        (i_units = 'Cup' or i_units = 'Pallet') and
        (i_size = 'medium' or i_size = 'large')
        ))) or
       (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'tomato' or i_color = 'chocolate') and 
        (i_units = 'Gram' or i_units = 'Ounce') and
        (i_size = 'medium' or i_size = 'large')
        ) or
        (i_category = 'Women' and
        (i_color = 'blanched' or i_color = 'plum') and
        (i_units = 'Lb' or i_units = 'Dram') and
        (i_size = 'economy' or i_size = 'extra large')
        ) or
        (i_category = 'Men' and
        (i_color = 'green' or i_color = 'floral') and
        (i_units = 'Unknown' or i_units = 'Bundle') and
        (i_size = 'N/A' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'thistle' or i_color = 'black') and
        (i_units = 'Ton' or i_units = 'Tbl') and
        (i_size = 'medium' or i_size = 'large')
        )))) > 0
 order by i_product_name
 limit 100;