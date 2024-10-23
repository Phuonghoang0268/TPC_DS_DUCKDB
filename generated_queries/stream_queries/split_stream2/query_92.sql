select  distinct(i_product_name)
 from item i1
 where i_manufact_id between 916 and 916+40 
   and (select count(*) as item_cnt
        from item
        where (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'forest' or i_color = 'firebrick') and 
        (i_units = 'Ounce' or i_units = 'Bunch') and
        (i_size = 'medium' or i_size = 'N/A')
        ) or
        (i_category = 'Women' and
        (i_color = 'moccasin' or i_color = 'hot') and
        (i_units = 'Dram' or i_units = 'Tbl') and
        (i_size = 'extra large' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'khaki' or i_color = 'green') and
        (i_units = 'Case' or i_units = 'Ton') and
        (i_size = 'small' or i_size = 'large')
        ) or
        (i_category = 'Men' and
        (i_color = 'chocolate' or i_color = 'lemon') and
        (i_units = 'N/A' or i_units = 'Pallet') and
        (i_size = 'medium' or i_size = 'N/A')
        ))) or
       (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'ivory' or i_color = 'peru') and 
        (i_units = 'Gram' or i_units = 'Gross') and
        (i_size = 'medium' or i_size = 'N/A')
        ) or
        (i_category = 'Women' and
        (i_color = 'navy' or i_color = 'papaya') and
        (i_units = 'Tsp' or i_units = 'Lb') and
        (i_size = 'extra large' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'dodger' or i_color = 'cyan') and
        (i_units = 'Each' or i_units = 'Unknown') and
        (i_size = 'small' or i_size = 'large')
        ) or
        (i_category = 'Men' and
        (i_color = 'rosy' or i_color = 'powder') and
        (i_units = 'Cup' or i_units = 'Box') and
        (i_size = 'medium' or i_size = 'N/A')
        )))) > 0
 order by i_product_name
 limit 100;