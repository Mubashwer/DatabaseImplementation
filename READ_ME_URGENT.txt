1)The system is designed so that registration of viewers is done offline. So in order
to add a new viewer, a player has to log in and go to the viewer's page in order to do
so.

2)Since maintaining venues was not part of the project specification, venues can only
be browsed.

3)Premium and Crowdfunding viewers can order videos. Players can directly see URLs.
Regular members need an access code in order to successfully place an order.

4)All foreign key deletes are "cascade" deletes. This is because only players can delete
any data and their judgement is trusted.

5)Please use Chrome (because CSS does not work properly in IE, date input is not supported in firefox (it acts as textbox there))

6)Primary keys in tables where it does not have any meaning, can not be changed. But e.g in PlayerAddress where
AddressStartDate is a pk, it can be changed. 

7)In order to place an order, click on the VideoID of a row in the table in videos page
