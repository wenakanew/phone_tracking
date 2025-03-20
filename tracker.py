import tkinter as tk
from tkinter import messagebox
import webbrowser
import phonenumbers  # Parses and validates international phone numbers
from phonenumbers import geocoder, carrier, is_valid_number
import folium  # Creates interactive maps
from opencage.geocoder import OpenCageGeocode  # Converts location to coordinates

# OpenCage API Key
API_KEY = "c428ac8c58ce441b80e7520744f42055"

def track_number():
    number = entry.get().strip()

    if not number:
        messagebox.showerror("Error", "❌ Please enter a phone number!")
        return

    # Try parsing the number
    try:
        check_number = phonenumbers.parse(number)
        if not is_valid_number(check_number):
            messagebox.showerror("Error", "❌ This phone number is not valid.")
            return
    except phonenumbers.phonenumberutil.NumberParseException:
        messagebox.showerror("Error", "❌ Invalid phone number format! Please check and try again.")
        return

    # Get location
    number_location = geocoder.description_for_number(check_number, "en")

    if not number_location:
        messagebox.showerror("Error", "❌ Could not determine location for this number.")
        return

    # Get network provider
    network = carrier.name_for_number(check_number, "en") or "Unknown"

    if not API_KEY:
        messagebox.showerror("Error", "❌ Missing OpenCage API key.")
        return

    # Convert location to coordinates using OpenCage API
    geocoder_map = OpenCageGeocode(API_KEY)

    try:
        results = geocoder_map.geocode(number_location)
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to connect to OpenCage API: {e}")
        return

    if results:
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']

        # Get detailed location information
        try:
            location = geocoder_map.reverse_geocode(lat, lng)
            if location:
                city = location[0]["components"].get('city') or \
                       location[0]["components"].get('town') or \
                       location[0]["components"].get('village') or \
                       location[0]["components"].get('municipality', 'Not Found')

                state = location[0]["components"].get('state') or \
                        location[0]["components"].get('region') or \
                        location[0]["components"].get('state_district', 'Not Found')

                result_text.set(f"📍 Location: {number_location}\n"
                                f"📶 Network: {network}\n"
                                f"🏛️ State: {state}\n"
                                f"🏙️ City: {city}")

                # Generate an interactive map
                map_location = folium.Map(location=[lat, lng], zoom_start=9)
                folium.Marker([lat, lng], popup=number_location).add_to(map_location)
                map_file = "mylocation.html"
                map_location.save(map_file)

                # Open the generated map in a web browser
                webbrowser.open(map_file)
                messagebox.showinfo("Map", f"🗺️ Map saved as {map_file} and opened in browser.")
            else:
                messagebox.showerror("Error", "❌ City not found.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error fetching location details: {e}")
    else:
        messagebox.showerror("Error", "❌ Could not retrieve location coordinates!")

# Create the main window
root = tk.Tk()
root.title("Phone Number Tracker")
root.geometry("450x250")  # Set window size

# Create and place the widgets
tk.Label(root, text="Enter phone number with country code (e.g., +254712345678):").pack(pady=10)
entry = tk.Entry(root, width=35)
entry.pack(pady=5)

tk.Button(root, text="Track", command=track_number, bg="#4CAF50", fg="white").pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", fg="#333", font=("Arial", 11))
result_label.pack(pady=10)

# Run the application
root.mainloop()

