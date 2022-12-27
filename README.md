# 'tiny beauty': CRM
#### Video Demo:  <URL HERE>
#### Description:
#### This is my final project for [Harvard_CS50](https://cs50.harvard.edu/x/2022/)
'tiny beauty' is a Flask web application for small beauty salon or beauty parlour. In present state it is kind of CRM-system (Customer Relationship Management). It is designed to keep track of our customers and services beeing provided for our customers.
### Usage
This app allows users, which are authorized employees of our beauty salon, to login for an account. When 'logged in' users may see the list of existing customers. It is an HTML table with every row representing a separate customer. Logged in users can search for existing customer, view and edit detailed info about each customer or add [the new one customer](the?). Within customer's info page a user can also view [orders history table](the?), add [a new customer's order](a?), view and edit existing customer's orders details.
#### customers.html
This page represents customers table. It is an HTML table. Every row holds data for a single customer in the columns: 'ID', 'Unique ID', 'First name', 'Last name', 'Email'. The 'View customer' column holds the button which redirects a user to the ['customer_info' page](#customer_infohtml) which is described [later](#customer_infohtml).
Atop of customers table search filters provided. If no user found by parameters provided and when nearby 'add new customer' button pressed then nonempty values of search fields will be added [to corresponding](the?) fields for a new customer.
#### customer_info.html
This page represents detailed info for [selected customer](a?) or [the new one](the?) beeing added. Customer's detailed info consists of the following fields: 'ID', 'Unique ID', 'First name', 'Last name', 'Gender', 'Email', 'Skin type', 'Contraindications', 'Precautions'. 'ID' field is immutable. 'Unique ID' field allows to identify several customers with same names, it is generated automaticaly but can be altered manualy. Manualy provided 'Unique ID' must be unique within all customers. 'Skin type' can be one of 5(five) default types (according to the American Academy of Dermatology): 'oily', 'dry', 'normal', 'combined' (oily+dry), 'sensitive'. Every visit of [the beauty](the?) salon by a customer is called 'Service order'. All visits of [the salon](the?) by [a customer](a?) are gathered in [the 'Customer orders'](the?) table of [the customer_info](the?) page. Each row represents [a separate](a?) service order and includes columns: 'ID', 'Number', 'Date', 'Skin condition', 'Beautician', 'Order status'. Where 'ID' is service order id, 'Number' is service order unique number for additional identifying of service orders, 'Date' is service order appointment date, 'Skin condition' represents skin condition as it was examined during [the visit](the?) by [the beautician](the?) which is mentioned in the 'Beautician' column. The 'View order' column holds [a button](a?) which redirects 
[a user to the]() ['service order details' page](#svc_order_detailshtml) which contains details of [the visit](the?).
#### svc_order_details.html
[the Order details](the?) page represents [a detailed info](a?) for [the selected order](the?) or [the new one](the?) beeing added. Basic information is devided into to areas: 'Order info' and 'Customer info'. Since this is order detail page 'Customer info' is immutable and is displayed here for beautcians' convenience. Particularly its' 'Contraindications' and 'Precautions' fields. 'Order info' area holds such data-fields which briefly describe particular order. 'ID' field is immutable. 'Unique ID' field is generated automaticaly but can be altered manualy. 'Order status' can have one of 3(three) default values: 'confirmed', 'rendered', 'canceled'. During assessment and treatment time [a beautician](a?) switches 'Order status' to 'rendered'. 'Order placed date' field is immutable and indicates when current order was created. 'Appointment date' field should match with actual start time and can be altered using datetime picker. 'Beautician' field indicates which therapist has provided treatment during current session. It is a selection field with list of all users who have the role 'beautician'. 'Description' field is for any additional important information regarding current treatment session to be mentioned by beautician. 'Complaints' field represents customers' literal description of complaints and reasons for treatment. 'Skin condition' field represents results of skin assessment by beautician. 'Order datails' table represents list of treatments which were actualy provided for customer during current session. The table content is updated using modal window by pushing the 'Select treatment' button. When finished treatment selection and 'Confirm selection' button pushed the table content is replaced by selected items.
Once a beautician has completed the initial treatment he introduces a customer the treatment plan as professional recommendations which include both services beeing stored in the 'Treatment plan' table and home care beeing stored in the 'Home care recommendations' table. Both 'Treatment plan' and 'Home care recommendations' are updated as 'Order datails' table is. I.e. using modal window by pushing the corresponding 'Select' button. To save order details' changes push the 'Save' button.
####
