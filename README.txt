# 4th_year_proj

what you need:
	- python 
	- linux (maybe)
	- sudo apt install sqlite3

usage:
	clone the repo to home
	cd ~/4th_year_proj/bin
	1. run server: ./server_recieve_data.py
	2. run client ./client_send_data_simulatiom.py 
	then raw_dat.db will be created into raw_data.db

to view data in db:
	sqlite3 raw_data.db
	SELECT * FROM raw_data;
	.quit


export db to csv:
	sqlite
	.header on
	.mode csv
	.once ./raw_data.csv
	SELECT * FROM raw_data;
	.quit
