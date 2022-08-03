# README.md

If you're here for **custom column mapping**, click [here](#custom-column-mapping).

1. [Software Presentation](#software-presentation)
2. [User Guide](#user-guide)
3. [Developer Guide](#developer-guide)

## Software Presentation

This software was built as a prototype to demonstrate the point of a *neat pile of charts* as in this [thesis](no-link-yet)

Upload your zoology register data to the app and use the different charts and numerous filters to visualise your registers through space and time lenses.
The software is designed to help your curate your data by finding domain-specific inconsistencies, it is therefore aimed at rather knowledgable users in their field.

## User Guide

- ### How to use the software

  Once you arrive on the web app page, it will ask you which app version you want, select it and press the "validate choice" button.
  
  You then arrive on the upload screen, press "browse files" and upload the right dataset (an excel file for Reptiles and Crustaceas, or a csv file for GBIF), once it's uploaded, press the "load application" button.
  
  After all this, you are on the working application, you have filters on the left bar (you can select and de-select orders, families and types by clicking on their colored icon), and 3 visualisations on the right.
  
  The top-left visualisation is the world map, the one on the top-right is a spatial visualisation and the bottom one is a temporal visualisation.
  You can change the spatial and temporal visualisations using the selectors in the middle of the web app, you can also control the time range of the data that you want to study using the time slider.

- ### Reptiles and Crustaceas

  The reptiles and crustaceas options have been tailored for Excel datasets used by specific experts, therefore they are not of use to the public.

- ### Custom Column Mapping

  ### How to upload your custom data:
  If you want to be able to upload your custom column mapping, on the web application you need to choose the 'GBIF' app version and ceck the 'use custom data and mapping' checkbox.
  On the next screen, you can upload your custom data in the first upload section, then on the right you can select what type of separator is used in your data (comma, semicolon, tab), and there is another upload section for your custom column mapping.
  Once this is done, you can press "load application".
  
  ### How to create your custom column mapping
  
  Now you need to understand how to map the columns of your dataset to the fields used by the applications.
  
  VERY IMPORTANT :
  **Have a look at the file custom_mapping.csv in the git 'ressources' folder. It is the one used by default when you do not provide any, let's explain what each of the columns does:**

  - #### columns **'field'** and **'name in your file'**:
  
    In the column **field** are all of the fields required by the application, for exemple 'collected_date' is a crucial information that this software uses for temporal visualisations.
    Maybe in your *own data* there is no such column as 'collected_date', let's say you have it under the name 'eventDate', then you would write 'eventDate' in the **name in your file** column just as it is done in the exemple file.
  
    Likewise, every **field** must be mapped to a **name in your file** for the software to know where to look at in your data.
  
    additionnal possible fields not present in the exemple file:
    ```
    first_name and last_name:
    If your file has two columns for name (a column for first name and a column for last name), instead of using the field 'collector_full_name', use both fields 'collector_first_name' and 'collector_last name' and don't forget to map them with your columns.

    In the same way, 'determinator_full_name' becomes 'determinator_first_name' and 'determinator_last_name'
    ```

  - #### column **'type'**:
    The type is a very important information, it helps the software perform useful transformation and treatment on your data.
    You have the choice between each of the following:
    
    `text : your column contains simple text like names, descriptions and so on`
    
        for exemple determinator_full_name will be a name, therefore it is textual information
    `integer : your column contains integers or categories encoded as integers`
    
        for exemple catalog_number will be an integer
    `float : your column contains decimal number such as 1036.43 or 0.3`
    
        for exemple the altitude will be a number it meters, it is a float
    `date : your column is a date in the format year/month/day`
    
        for exemple collected_date is a date, make sure it is in year/month/day format

  - #### column **'selected'**:
    The selected column defines which columns are kept after the data treatment (some columns such as dates are only useful during the treatment and are dropped after, because the software extracted the years and months)

    You should just leave them as in the examples, and if you don't know just leave everything selected (TRUE), it will not break the software to have too much columns selected.

  - #### column **'description'**:
    If you need to add some notes for yourself in the file, it is not used by the software.

## Developer Guide
  > (documentation in progress)
  
  There are 3 app_versions: reptiles, crustaceas and GBIF.
  
- ### How the software works
  
  This software is using the [streamlit framework](https://docs.streamlit.io/), which is a python framework to build web applications.
  It works by running the streamlit_app.py python file, and everytime an [input](https://docs.streamlit.io/library/api-reference/widgets) is used, the streamlit_app.py file is re-run and variables are updated.
  
  The Viz_Zoo software loads the uploaded data and stores it as a pandas DataFrame, whenever the user applies any filter (time slider, order and family selectors, etc) the data is filtered, and [altair](https://altair-viz.github.io/) visualisations are applied on the filtered data and are displayed using Streamlit's API.
  
  Streamlit only has a few input widgets (buttons, selectors, ...) but you can make your own custom components using React.js, this is how the filter widgets on the left sidebar have been created. Those selectors let you filter for order, family, type.
  
  **A functions analysis is available [here](documentation/functions_analysis.drawio.svg)**

  #### graph_dict.py
  Python file that indicates for each app_version, which altair visualisations are available in the web app selectors.
  
      for exemple, crustaceas app_version does not have access to the altitude graphs, as they only have depth information
  For each app_version, you will need to give them access to any new altair visualisation you create by adding their name in this file.
  

  #### column_dict.py
  Column mappings used when no custom one is provided, there is one for each app_version.
  These mappings have been tailored for specific excel files used by experts, make sure changing this file does not break the software.
