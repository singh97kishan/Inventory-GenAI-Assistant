few_shots = [
    {
        'Question': "What is the price of inventory for all ipad pro?" ,
        'SQLQuery' : "select sum(price * stock_quantity) from apple_data where product_name = 'iPad Pro';",
        'SQLResult' : "Result of the SQL query",
        'Answer': '31960'
    },

        {
        'Question': "If we have to sell all the iphones today with discounts applied, how much revenue our store will generate (post discounts)?" ,
        'SQLQuery' : "select sum(t1.total_amount * ((100 - t2.discount_perc)/100)) as total_revenue from (select product_id, sum(price*stock_quantity) as total_amount from apple_data where product_category='iPhone' group by product_id) t1 left join discounts t2 on t1.product_id = t2.product_id;",
        'SQLResult' : "Result of the SQL query",
        'Answer': '301854.4'
    },

    {
        'Question': "How many airpods do we have available?" ,
        'SQLQuery' : "select sum(stock_quantity) from apple_data where product_category='Airpods';",
        'SQLResult' : "Result of the SQL query",
        'Answer': '495'
    }
]