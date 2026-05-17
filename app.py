import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="E-Commerce System", page_icon="🛒")

# Login System
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Login to E-Commerce System")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Galat username ya password")

    st.info("Demo Login: username = admin, password = 1234")

def main_app():
    st.title("E-Commerce Shopping System 🛒")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.write(f"Welcome, admin!")

    # Products ka data with images
    products = {
        "Laptop": {"price": 50000, "img": "https://cdn-icons-png.flaticon.com/512/428/428001.png"},
        "Mobile": {"price": 20000, "img": "https://cdn-icons-png.flaticon.com/512/0/191.png"},
        "Headphones": {"price": 3000, "img": "https://cdn-icons-png.flaticon.com/512/3791/3791461.png"},
        "Smart Watch": {"price": 5000, "img": "https://cdn-icons-png.flaticon.com/512/3042/3042679.png"},
        "Keyboard": {"price": 1500, "img": "https://cdn-icons-png.flaticon.com/512/118/118734.png"}
    }

    # Cart banane ke liye session
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # Available Products dikhana with photo
    st.subheader("Available Products")
    cols = st.columns(5)
    for idx, (name, data) in enumerate(products.items()):
        with cols[idx]:
            st.image(data["img"], width=80)
            st.write(f"**{name}**")
            st.write(f"₹{data['price']}")

    # Search Product
    st.subheader("Search Product")
    search = st.text_input("Search Product")
    if search:
        filtered = {k:v for k,v in products.items() if search.lower() in k.lower()}
        for name, data in filtered.items():
            st.write(f"{name} - ₹{data['price']}")

    # Select Product
    st.subheader("Add to Cart")
    product = st.selectbox("Select Product", list(products.keys()))
    quantity = st.number_input("Enter Quantity", min_value=1, value=1)

    if st.button("Add to Cart"):
        st.session_state.cart.append({
            "Product": product,
            "Quantity": quantity,
            "Price": products[product]["price"],
            "Total": products[product]["price"] * quantity
        })
        st.success(f"{product} added to cart!")

    # Cart dikhana
    st.subheader("Your Cart")
    if len(st.session_state.cart) == 0:
        st.write("Cart is empty")
    else:
        # Remove button ke liye har item alag se
        for i, item in enumerate(st.session_state.cart):
            col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
            with col1:
                st.write(item["Product"])
            with col2:
                st.write(f"Qty: {item['Quantity']}")
            with col3:
                st.write(f"₹{item['Price']}")
            with col4:
                st.write(f"₹{item['Total']}")
            with col5:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()

        # Total bill
        total_bill = sum(item['Total'] for item in st.session_state.cart)
        st.subheader(f"Total Bill: ₹{total_bill}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Cart"):
                st.session_state.cart = []
                st.rerun()
        with col2:
            if st.button("Checkout"):
                st.balloons()
                st.success("Order Placed Successfully!")
                st.session_state.cart = []

# Login check
if st.session_state.logged_in:
    main_app()
else:
    login_page()