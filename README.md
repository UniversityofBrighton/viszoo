# README.md

If you're here for **[custom column mapping](#custom-column-mapping)**

1. [Software Presentation](#software-presentation)
2. [User Guide](#user-guide)
3. [Developer Guide](#developer-guide)

## Software Presentation

This software was built as a prototype to demonstrate the point of a *neat pile of charts* as in this [thesis](no-link-yet)

Upload your zoology register data to the app and use the different charts and numerous filters to visualise your registers through space and time lenses.
The software is designed to help your curate your data by finding domain-specific inconsistencies, it is therefore aimed at rather knowledgable users in their field.

## User Guide

- ### Reptiles and Crustaceas

  The reptiles and crustaceas options have been tailored for Excel datasets used by specific experts, therefore they are not of use to the public.

- ### Custom Column Mapping

  Have a look at the file custom_mapping.csv in the ressources folder. (It is the one used by default when you do not provide any for GBIF data).
  If you want to be able to upload your custom column mapping, you need to choose the 'GBIF' app version and ceck the 'use custom data and mapping' checkbox

  #### 'field' and 'name in your file':
  All fields in the "field" column need a mapping in your file (the "name in your file" column), this means they need to know in which column of your file they are getting the data.

  The fields are required information for the software to work, therefore you need all of them to be mapped to your file columns.

  For example here the field "collector_full_name" is mapped to the column "recordedBy" which is the name of the column for the collector name in GBIF data.

  #### first_name and last_name:
  If your file has two columns for name (a column for first name and a column for last name), instead of using the field 'collector_full_name', use both fields 'collector_first_name' and 'collector_last name' and don't forget to map them with your columns.
  
  In the same way, 'determinator_full_name' becomes 'determinator_first_name' and 'determinator_last_name'


  #### 'type':
  The type is a very important information, it helps the software perform useful transformation and treatment on your data.
  - text : your column contains simple text like names, descriptions and so on
  - integer : your column contains integers or categories encoded as integers
  - float : your column contains decimal number such as 1036.43 or 0.3
  - date : your column is a date in the format year/month/day

  #### 'selected':
  The selected column defines which columns are kept after the data treatment (some columns such as dates are only useful during the treatment and are dropped after, because the software extracted the years and months)

  You should just leave them as in the examples, and if you don't know just leave everything on selected, it will not break the software (as if you unselect the wrong one, it will break)

  #### 'description':
  If you need to add some notes for yourself in the file.

## Developer Guide

  There are 3 app_versions: reptiles, crustaceas and GBIF.

- ### graph_dict.py
  Python file that indicates for each app_version, which graphs are available.

- ### column_dict.py
  Column mappings used when no custom one is provided, there is one for each app_version
