# 'tiny beauty': CRM
## This is my final project for [Harvard_CS50](https://cs50.harvard.edu/x/2022/)
'tiny beauty' is a Flask web application for small beauty salon or beauty parlour. In present state it is kind of CRM-system (Customer Relationship Management). It is designed to keep track of our customers and services beeing provided for our customers.
### Usage
This app allows users, which are authorized employees of our beauty salon, to login for an account. When 'logged in' users may see the list of existing customers. It is an HTML table with every row representing a separate customer. Logged in users can search for existing customer, view and edit detailed info about each customer or add [the new one customer](). Within customer's info page a user can also view [orders history table](the?), add [a new customer's order](a?), view and edit existing customer's orders details.
#### customers.html
This page represents customers table. It is an HTML table. Every row holds data for single customer in the columns: 'ID', 'Unique ID', 'First name', 'Last name', 'Email'. The 'View customer' column holds the button which redirects a user to the ['customer_info' page](#customer_info.html) which is described [later](#customer_info).

#### customer_info.html
............................................................................................................................................................................................................................
Logged in users can quote stocks (i.e. look up a stocks' current price), 'buy' and 'sell' stocks (quoted since when registered each user provided Total 10000 points which are not real money and stocks beeing bought or sold are virtual). Any way quoted prices remain actual. Logged in users can also see transactions history (HTML table with detailed information of every 'buy' and every 'sell').