# **Phone Number Tracker**

This **Phone Number Tracker** program is a Python application built using **Tkinter**, **phonenumbers**, **OpenCage API**, and **Folium** to retrieve location details of a given phone number and display its approximate location on an interactive map.

## **🔹 How the Program Works**

### **1️⃣ User Interface (Tkinter)**
- The program creates a simple **GUI (Graphical User Interface)** using Tkinter.
- The user **enters a phone number** in the input field and clicks the `"Track"` button.
- The program processes the phone number and displays:
  - 🌍 **Geographical Location (Country, City, State)**
  - 📶 **Network Provider (Safaricom, Airtel, etc.)**
  - 🗺️ **A Map with the Tracked Location**

### **2️⃣ Processing the Phone Number**
- The **entered phone number** is retrieved from the input field.
- The program checks if the input is empty and **displays an error** if nothing is entered.
- The number is then **parsed and validated** using the `phonenumbers` library:
  ```python
  check_number = phonenumbers.parse(number)
  if not is_valid_number(check_number):
      messagebox.showerror("Error", "❌ This phone number is not valid.")
      return
  ```
- If the number format is invalid, an **error message** is shown.

### **3️⃣ Extracting Location & Network Provider**
- The **phonenumbers** module helps extract:
  - **Country** using `geocoder.description_for_number()`
  - **Network Provider** using `carrier.name_for_number()`

Example:
```python
number_location = geocoder.description_for_number(check_number, "en")
network = carrier.name_for_number(check_number, "en") or "Unknown"
```
- If the **location is missing**, an error is displayed.

### **4️⃣ Converting Location to Coordinates (OpenCage API)**
- The **OpenCage API** is used to **convert** the location (country/city) into **latitude and longitude coordinates**.
- This helps place the location on a map.
- The API **sends a request to OpenCage** and retrieves **coordinates**:
  ```python
  geocoder_map = OpenCageGeocode(API_KEY)
  results = geocoder_map.geocode(number_location)
  ```
- If coordinates are **not found**, the program **displays an error**.

### **5️⃣ Generating & Displaying the Map (Folium)**
- The **Folium** library creates an **interactive map**.
- The program:
  - Centers the map on the **retrieved coordinates**.
  - Adds a **marker** to indicate the phone number's location.
  - Saves the map as an **HTML file** and **opens it in the browser**.
  ```python
  map_location = folium.Map(location=[lat, lng], zoom_start=9)
  folium.Marker([lat, lng], popup=number_location).add_to(map_location)
  map_location.save("mylocation.html")
  webbrowser.open("mylocation.html")
  ```
- The map **automatically opens in the web browser**.

## **🔹 Program Flow (Step-by-Step Execution)**
1. **User enters** a phone number (e.g., `+254712345678`).
2. Program **validates** the number.
3. If valid, it **retrieves**:
   - 🌍 **Country**
   - 📶 **Network Provider**
4. Uses **OpenCage API** to **convert the location to GPS coordinates**.
5. Creates an **interactive map** using Folium.
6. The **map is displayed** in the browser.

## **🔹 Example Output**
If the user enters `+254712345678`, the program may display:
```
📍 Location: Kenya
📶 Network: Safaricom
🏛️ State: Nairobi County
🏙️ City: Nairobi
```
- A **map opens in the browser**, showing **Nairobi's location**.

## **🔹 Key Features**
✅ **Validates phone numbers** to prevent incorrect inputs.  
✅ **Displays network provider** (Safaricom, Airtel, etc.).  
✅ **Uses an API to get precise GPS coordinates**.  
✅ **Generates an interactive map** for visual tracking.  

## **🛠️ Potential Improvements**
🚀 **Add live tracking** (if you integrate with a GPS tracking system).  
🌐 **Support multiple APIs** (e.g., Google Maps API for better results).  
📊 **Display additional details** (e.g., time zone, ISP provider).  

## **🔹 Final Thoughts**
This program **does not track real-time movement**; it only provides an **approximate registered location** of a phone number based on the country and city. However, it's useful for **basic number lookup and mapping**. 🚀

