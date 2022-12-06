# 'tiny beauty': CRM
## This is my final project for [Harvard_CS50](https://cs50.harvard.edu/x/2022/)
'tiny beauty' is a Flask web application for small beauty salon or beauty parlour. In present state it is kind of CRM-system (Customer Relationship Management). It is designed to keep track of our customers and services beeing provided for our customers.
### Usage
This app allows users, which are authorized employees of our beauty salon, to login for an account. When 'logged in' users may see the list of existing customers. It is an HTML table with every row representing a separate customer. Logged in users can search for existing customer, view and edit detailed info about each customer or add [the new one customer](the?). Within customer's info page a user can also view [orders history table](the?), add [a new customer's order](a?), view and edit existing customer's orders details.
#### customers.html
This page represents customers table. It is an HTML table. Every row holds data for a single customer in the columns: 'ID', 'Unique ID', 'First name', 'Last name', 'Email'. The 'View customer' column holds the button which redirects a user to the ['customer_info' page](#customer_infohtml) which is described [later](#customer_infohtml).
Atop of customers table search filters provided. If no user found by parameters provided and when nearby 'add new customer' button pressed then nonempty values of search fields will be added [to corresponding](the?) fields for a new customer.
#### customer_info.html
This page represents detailed info for [selected customer](a?) or [the new one](the?) beeing added. Customer's detailed info consists of the following fields: 'ID', 'Unique ID', 'First name', 'Last name', 'Email', 'Skin type', 'Contraindications', 'Skin condition', 'Additional info'. 'ID' field is immutable. 'Unique ID' field allows to identify several customers with same names, it is generated automaticaly but can be altered manualy when manualy provided is unique either. 'Skin type' can be one of 5(five) default types (according to the American Academy of Dermatology): 'oily', 'dry', 'normal', 'combined' (oily+dry), 'sensitive'. 
