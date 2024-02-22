data_dict = """
TABLE NAME : apple_data
TABLE DESCRIPTION: This is the product inventory table which has details at product level.
COLUMN DESCRIPTION:
- product_id : unique ID for each product.
- product_category : It is a product hierarchy column which tells which category the given product belongs to.
- product_name : This column tells the name of the product for the given product_id.
- price: This is the price per unit for the given product_id.
- stock_quantity : Total units left in stock or units available for the a given product_id.

TABLE NAME : discounts
TABLE DESCRIPTION: This is the discount table which has all the discounts related information at product_id level.
COLUMN DESCRIPTION:
- product_id : Unique product ID to identify the product.
- discount_perc : Discount percentage for a product. Value of 5 represents 5 percentage discount on the unit price of the product. 

"""

few_shots = [
    {
        'Question': "What is the price of inventory for all ipad pro?" ,
        'SQLQuery' : "select product_name as ProductName, sum(price * stock_quantity) as TotalPrice from apple_data where product_name = 'iPad Pro';",
    },

    {
        'Question': "If we have to sell all the iphones today with discounts applied, how much revenue our store will generate (post discounts)?" ,
        'SQLQuery' : """select t1.product_category as ProductCategory, sum(t1.total_amount * ((100 - t2.discount_perc)/100)) as TotalRevenue
                        from (
                            select product_id, product_category, sum(price*stock_quantity) as total_amount
                            from apple_data where product_category='iPhone'
                            group by product_id, product_category
                        ) t1
                        left join discounts t2 on t1.product_id = t2.product_id
                        group by t1.product_category;"""
    },

    {
        'Question': "How many airpods do we have available?" ,
        'SQLQuery' : "select product_category as ProductCategory, sum(stock_quantity) as Quantity from apple_data where product_category='Airpods';"
    },

    {
        'Question': "How many iPhones do we have left in stock?" ,
        'SQLQuery' : "select product_category as ProductCategory, sum(stock_quantity) as Quantity from apple_data where product_category='iPhone';"
    },

        {
        'Question': "How many iPad Pro are left stock?" ,
        'SQLQuery' : "select product_name as ProductName, sum(stock_quantity) as Quantity from apple_data where product_name='iPad Pro';"
    },


    {
        'Question': 'What is the price of iphone 13?',
        'SQLQuery': """select product_name as ProductName, price as Price 
                        from apple_data where product_name= 'iPhone 13';"""
    },

    {
        'Question': 'What is the discounted price for iPhone 13?',
        'SQLQuery': """
                    select a.product_name, a.price, (a.price - (a.price* d.discount_perc)/100) as DiscountedPrice
                    from apple_data a join discounts d on a.product_id = d.product_id
                    where a.product_name = 'iPhone 13';    
                    """
    },

    {
        'Question': "What is the discount present on Airpods Max",
        'SQLQuery': """select a.product_name, d.discount_perc
                     from apple_data a join discounts d on a.product_id = d.product_id
                      where a.product_name = 'Airpods Max';
                    """
    }
]

generic_prompts = [
    "Hi",
    "Hey",
    "Hello",
    "How are you?",
    "Hey there",
    "I have a ques",
    "I want to ask something"
]

mysql_prompt = f"""

You are a MySQL expert and you have to answer using SQL queries for the question using DATA DICTIONARY : {data_dict}.

Follow the RULES mentioned below while displaying the answer:
1. Give only SQL Query as response/output.
2. Do not do any modification operations like Alter, Update, Delete or Truncate.
3. Use only columns and tables mentioned in the data dictionary.
4. If asked about revenue or Sales, return the query with the product hierarchy level like product_category and product_name.
5. Output should have unique records only.

IMPORTANT: Give only SQL Query as response.

INSTRUCTIONS: Don't use tab or extra spaces while generating queries.

Use the following format:

Question: User Question
SQLQuery: SQL query to return

ADDITIONAL INFORMATION:
1. If any Product name or category is not mentioned in the prompt, consider the previous product info from chat history.
2. If the prompt seems to have irrelevant context or some personal question which do not any relation with our table schema, respond "Cannot process the request, please ask relevant question" 
"""