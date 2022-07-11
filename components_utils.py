import streamlit as st
import os
import streamlit.components.v1 as components


def load_components():
  # loading my components
  root_dir = os.path.dirname(os.path.abspath(__file__))

  build_dir_family = os.path.join(root_dir, "components"+os.sep+"family_selector_component"+os.sep+"family_selector"+os.sep+"frontend"+os.sep+"build")

  family_selector_component = components.declare_component(
    "family_selector",
    path=build_dir_family,
  )

  build_dir_type = os.path.join(root_dir, "components"+os.sep+"type_selector_component"+os.sep+"type_selector"+os.sep+"frontend"+os.sep+"build")

  type_selector_component = components.declare_component(
    "type_selector",
    path=build_dir_type,
  )

  # functions definition
  def family_selector(families, key):
      component_value = family_selector_component(familias = families, default=families, key=key)
      return component_value

  def type_selector(types, key):
    component_value = type_selector_component(types = types, default = types, key=key)
    return component_value

  return family_selector, type_selector

from data_utils import create_color_palettes

def get_selectors(data, app_version, colors):

# loading families informations and color
  families, orders = colors
  st.session_state["families"] = families
  families_name = list(families.keys())
  families_color = list(families.values())
  list_families = list()


  # creates the family list for the family selector
  for index in range(len(families_name)):
    fam = dict()
    fam["name"] = families_name[index]
    fam["color"] = families_color[index]
    fam["selected"] = True
    list_families.append(fam)

  st.session_state["orders"] = orders
  orders_name = list(orders.keys())
  orders_color = list(orders.values())
  list_orders = list()

  # creates the family list for the family selector
  for index in range(len(orders_name)):
    ord = dict()
    ord["name"] = orders_name[index]
    ord["color"] = orders_color[index]
    ord["selected"] = True
    list_orders.append(ord)

  # handling Types, creating the Type list for the Type selector
  type_names = data['type_status'].unique()
  list_types = list()
  for index in range(len(type_names)):
    new_type = dict()
    new_type['name'] = str(type_names[index])
    new_type['shape'] = "square"
    new_type['selected'] = True
    list_types.append(new_type)



  if app_version == 'reptiles':
    return [
      {
        'name':'order',
        'selector': 'family_selector',
        'list':list_orders
      },
      {
        'name':'family',
        'selector': 'family_selector',
        'list':list_families
      },
      {
        'name':'type_status',
        'selector': 'type_selector',
        'list':list_types
      }
    ]
  elif app_version == 'crustaceas':
    return [
      {
        'name':'infraorder',
        'selector': 'family_selector',
        'list':list_orders
      },
      {
        'name':'family',
        'selector': 'family_selector',
        'list':list_families
      },
      {
        'name':'type_status',
        'selector': 'type_selector',
        'list':list_types
      },
    ]
  elif app_version == 'GBIF':
    return [
      {
        'name':'order',
        'selector': 'family_selector',
        'list':list_orders
      },
      {
        'name':'family',
        'selector': 'family_selector',
        'list':list_families
      },
      {
        'name':'type_status',
        'selector': 'type_selector',
        'list':list_types
      }
    ]

def get_filters_out(selectors_components):
  list_selector_output = list()
  for selector in selectors_components:
    st.write(selector['name'])
    selector['list'] = st.session_state[selector['selector']](selector['list'], selector['name'])
    list_selector_output.append((selector['name'], selector['list']))

  list_filter_out = list()
  for list_sel in list_selector_output:
    filter_out = list()
    for occ in list_sel[1]:
      if not(occ['selected']):
        filter_out.append(occ['name'])
    list_filter_out.append({'name_column':list_sel[0], 'filter':filter_out})

  return list_filter_out