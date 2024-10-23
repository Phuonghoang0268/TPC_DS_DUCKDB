select  distinct(i_product_name)
 from item i1
 where i_manufact_id between 925 and 925+40 
   and (select count(*) as item_cnt
        from item
        where (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'almond' or i_color = 'pink') and 
        (i_units = 'Tbl' or i_units = 'Each') and
        (i_size = 'medium' or i_size = 'large')
        ) or
        (i_category = 'Women' and
        (i_color = 'hot' or i_color = 'cream') and
        (i_units = 'Pound' or i_units = 'Cup') and
        (i_size = 'extra large' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'cornsilk' or i_color = 'blue') and
        (i_units = 'Gross' or i_units = 'Dozen') and
        (i_size = 'N/A' or i_size = 'economy')
        ) or
        (i_category = 'Men' and
        (i_color = 'navy' or i_color = 'light') and
        (i_units = 'N/A' or i_units = 'Lb') and
        (i_size = 'medium' or i_size = 'large')
        ))) or
       (i_manufact = i1.i_manufact and
        ((i_category = 'Women' and 
        (i_color = 'gainsboro' or i_color = 'rosy') and 
        (i_units = 'Pallet' or i_units = 'Ton') and
        (i_size = 'medium' or i_size = 'large')
        ) or
        (i_category = 'Women' and
        (i_color = 'magenta' or i_color = 'lavender') and
        (i_units = 'Case' or i_units = 'Dram') and
        (i_size = 'extra large' or i_size = 'petite')
        ) or
        (i_category = 'Men' and
        (i_color = 'brown' or i_color = 'smoke') and
        (i_units = 'Unknown' or i_units = 'Box') and
        (i_size = 'N/A' or i_size = 'economy')
        ) or
        (i_category = 'Men' and
        (i_color = 'honeydew' or i_color = 'sienna') and
        (i_units = 'Oz' or i_units = 'Bunch') and
        (i_size = 'medium' or i_size = 'large')
        )))) > 0
 order by i_product_name
 limit 100;