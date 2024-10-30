import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Ustawienie strefy czasowej Warszawy
tz = pytz.timezone('Europe/Warsaw')

# Dane restauracji
restaurants = {
    'Włoska Restauracja': {
        'address': 'ul. Marszałkowska 1, Warszawa',
        'opening_hours': {'open': 12, 'close': 22},  # Otwarta od 12:00 do 22:00
        'menu': {
            'Pizza Margherita': {'price': 25, 'extras': ['extra cheese', 'extra sauce']},
            'Spaghetti Carbonara': {'price': 30, 'extras': ['extra bacon', 'extra cheese']},
            'Tiramisu': {'price': 15, 'extras': []}
        },
        'map_url': 'https://goo.gl/maps/example1'
    },
    'Polska Restauracja': {
        'address': 'ul. Nowy Świat 2, Warszawa',
        'opening_hours': {'open': 10, 'close': 20},  # Otwarta od 10:00 do 20:00
        'menu': {
            'Schabowy z ziemniakami': {'price': 35, 'extras': ['extra ziemniaki', 'extra surówka']},
            'Pierogi ruskie': {'price': 20, 'extras': ['extra cebula', 'extra śmietana']},
            'Sernik': {'price': 10, 'extras': []}
        },
        'map_url': 'https://goo.gl/maps/example2'
    }
}

# Funkcja sprawdzająca czy restauracja jest otwarta
def is_open(restaurant):
    current_time = datetime.now(tz).hour
    return restaurants[restaurant]['opening_hours']['open'] <= current_time < restaurants[restaurant]['opening_hours']['close']

# Formularz wyboru restauracji
st.title("Złóż zamówienie w swojej ulubionej restauracji")
restaurant_choice = st.selectbox("Wybierz restaurację", list(restaurants.keys()))

# Wyświetlanie szczegółów restauracji
restaurant_info = restaurants[restaurant_choice]
st.write(f"Adres: {restaurant_info['address']}")
st.write(f"Godziny otwarcia: {restaurant_info['opening_hours']['open']}:00 - {restaurant_info['opening_hours']['close']}:00")
st.write(f"[Zobacz na mapie]({restaurant_info['map_url']})")

# Sprawdzanie, czy restauracja jest otwarta
if not is_open(restaurant_choice):
    st.error("Restauracja jest zamknięta, nie można złożyć zamówienia.")
else:
    st.success("Restauracja jest otwarta, możesz złożyć zamówienie.")
    
    # Formularz wyboru pozycji z menu
    st.subheader(f"Menu - {restaurant_choice}")
    
    order = {}
    total_price = 0
    
    for item, details in restaurant_info['menu'].items():
        # Wybór ilości dań
        quantity = st.number_input(f"{item} - {details['price']} PLN", min_value=0, max_value=10, step=1)
        if quantity > 0:
            order[item] = {'quantity': quantity, 'extras': [], 'price': details['price'] * quantity}
            total_price += details['price'] * quantity
            
            # Wybór dodatków, jeśli są dostępne
            if details['extras']:
                extras = st.multiselect(f"Wybierz dodatki do {item}", details['extras'])
                order[item]['extras'] = extras
    
    # Wyświetlenie podsumowania zamówienia
    if st.button("Złóż zamówienie"):
        if total_price > 0:
            st.write("Twoje zamówienie:")
            for item, details in order.items():
                st.write(f"{item} x{details['quantity']}")
                if details['extras']:
                    st.write(f"Dodatki: {', '.join(details['extras'])}")
            st.write(f"Łączna cena: {total_price} PLN")
        else:
            st.warning("Nie wybrałeś żadnych dań.")
