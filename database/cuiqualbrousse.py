#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

# Constants to adjust to CIQUAL csv file
CSV_PATH='db_ciqual.csv'
FIRST_NUTRIENT_INDEX=10
LAST_NUTRIENT_INDEX=67


# Print 'create table' statements
print("""
    create table grp (
        id text primary key,
        name text
    );
""")
print("""
    create table food (
        id text primary key,
        name text,
        grp_id text not null references grp(id) on delete cascade
    );
""")
print("""
    create table nutrient (
        id serial primary key,
        name text
    );
""")
print("""
    create table nutdata (
        id serial primary key,
        food_id text not null references food(id) on delete cascade,
        nutrient_id integer not null references nutrient(id) on delete cascade,
        value text
    );
""")

# Pass #1: create groups and a list of already created groups
already_created_group_codes = []
with open('db_ciqual.csv', newline='') as csvfile:
    # read csv lines as dictionaries
    csv_reader = csv.DictReader(csvfile, delimiter=';')
    for row in csv_reader:
        alim_grp_code = row['alim_grp_code']
        alim_grp_nom_fr = row['alim_grp_nom_fr']

        # check if this group already exists
        if not alim_grp_code in already_created_group_codes:
            # print insert statement
            print(f"insert into grp (id, name) values ('{alim_grp_code}', '{alim_grp_nom_fr}');")
            already_created_group_codes.append(alim_grp_code)


# Pass #2: create foods
with open(CSV_PATH, newline='') as csvfile:
    # read csv lines as dictionaries
    csv_reader = csv.DictReader(csvfile, delimiter=';')
    for row in csv_reader:
        alim_code = row['alim_code']
        alim_nom_fr = row['alim_nom_fr']
        alim_grp_code = row['alim_grp_code']

        # print insert statement
        print(f"insert into food (id, name, grp_id) values ('{alim_code}', '{alim_nom_fr}', '{alim_grp_code}');")

 

# Pass #3: create nutrients in database, and a dictionnary nutrient_index => nutrient_id
nutrient_index_range = range(FIRST_NUTRIENT_INDEX, LAST_NUTRIENT_INDEX)
nutrient_dict = {}
nutrient_id = 1
with open(CSV_PATH, newline='') as csvfile:
    # read csv lines as arrays
    csv_reader = csv.reader(csvfile, delimiter=';')
    # read only the first line (column names)
    row = next(csv_reader)
    for nutrient_index in nutrient_index_range:
        nutrient_name = row[nutrient_index]
        # print insert statement
        print(f"insert into nutrient (id, name) values ('{nutrient_id}', '{nutrient_name}');")
        # fill nutrient_index => nutrient_id dictionary
        nutrient_id += 1
        nutrient_dict[nutrient_index] = nutrient_id


# Pass #4: create food/nutrient values
first_row = True
with open(CSV_PATH, newline='') as csvfile:
    # read csv lines as arrays
    csv_reader = csv.reader(csvfile, delimiter=';')
    for row in csv_reader:
        if first_row:
            # skip first line (column names)
            first_row = False
            continue
        else:
            alim_code = row[6]
            for nutrient_index in nutrient_index_range:
                # get nutrient_id from dictionnary
                nutrient_id = nutrient_dict[nutrient_index]
                value = row[nutrient_index]
                print(f"insert into nutdata (food_id, nutrient_id, value) values ('{alim_code}', '{nutrient_id}', '{value}');")