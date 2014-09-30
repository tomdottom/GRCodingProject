#GRCodingProject

For the sake of speed the project has been built using Django. The sole reason for doing this is my familiarity with it's ORM. Admittedly and db wasn't entirely necessecary to complete the given task, but was useful.

##maitre d'table

The main controller is `maitre_d_table` which has two methods: 

	maitre_d_table.reserve_table(restaurant_name, dt, people)

and

	maitre_d_table.restaurant_report(restaurant_name)
	
##Setup and tests

In `/project` install requirments (ideally with a venv)

	pip install requirements.txt 

Run the tests

	python manage.py test

Setup a db with some fixtures

	python manage.py syncdb
	python manage.py loaddata restaurant/fixtures/restaurants.json

'Le Coch' is a small restaurant with two 2 seater tables and 2 four seater tables
	
Use maitre d'table

	python manage.py shell
	
	from datetime import date, datetime
	import maitre_d_table
	
	maitre_d_table.reserve_table('Le Coch', datetime(2014, 9, 28, 12), 2)
	>> 1
	maitre_d_table.reserve_table('Le Coch', datetime(2014, 9, 28, 12), 2)
	>> 2
	maitre_d_table.reserve_table('Le Coch', datetime(2014, 9, 28, 12), 4)
	>> 3
	maitre_d_table.reserve_table('Le Coch', datetime(2014, 9, 28, 12), 4)
	>> 4
	
	maitre_d_table.reserve_table('Le Coch', datetime(2014, 9, 28, 12), 20)
	>> ReservationNotPossibleError: Not enough tables available to accomodate 20 people
	
	maitre_d_table.restaurant_report('Le Coch', date(2014, 9, 28))
	>> {'covers': 12}
	

##Known edges cases in code

The table packing algorithm is naive to the fact that some tables may already be seated. Currently it is possible for reservations to be made such that, on the arrival of a new table, all tables would have to stand and rearrange themselves for seating to be possible.

##Missing `maitre_d_table` features
- Creation/deletion/modification of restaurants.
- Modification/deletion of reservations.
- Extended reporting tools (ie. list reservartions for the day)

##Other Notes
The table packing algorithm may be a bit more opaque than I intended. It's basic operation can be summerised as follows:

- Create a new potential reservation
- Retrieve all current reservations which over lap the new reservation
- Find exact matches for single tables
- Find exact matches for combinations of tables
- For increasing numbers of spare seats
	- Find matches on single tables
	- Find matches on combination of tables