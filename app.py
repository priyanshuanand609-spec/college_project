import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# ==========================================
# 1. PAGE AND THEME CONFIGURATION
# ==========================================
st.set_page_config(page_title="Cloud Kitchen MIS & Consumer Portal", layout="wide")

# Custom CSS injection UI ko attractive banane ke liye
st.markdown("""
    <style>
        .main-header { font-family: 'Helvetica Neue', Arial; color: #1e3a8a; font-weight: bold; text-align: center; margin-bottom: 5px; }
        .sub-header { font-family: 'Arial'; color: #475569; text-align: center; margin-bottom: 25px; }
        .food-card { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 18px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 15px; }
        .metric-container { background-color: #f8fafc; border-left: 5px solid #3b82f6; padding: 15px; border-radius: 6px; }
        .macro-tag { background-color: #f0fdf4; color: #166534; font-size: 11px; padding: 2px 6px; border-radius: 4px; font-weight: bold; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. FILE MANAGEMENT (Database CSVs)
# ==========================================
ORDER_FILE = 'orders_data.csv'
REVIEW_FILE = 'reviews_data.csv'


def initialize_file(filename, column_list):
    if not os.path.exists(filename):
        pd.DataFrame(columns=column_list).to_csv(filename, index=False)


initialize_file(ORDER_FILE, ['Timestamp', 'Customer Name', 'Dish', 'Quantity', 'Total Price'])
initialize_file(REVIEW_FILE, ['Timestamp', 'User Name', 'Dish Sampled', 'Stars', 'Comments'])

# ==========================================
# 3. COMPREHENSIVE MENU (With Working Image Links)
# ==========================================
menu = {
    "Paneer Tikka": {
        "price": 250, "type": "Veg", "desc": "Smoky clay-oven grilled cottage cheese chunks spiced deeply.",
        "protein": "18g", "calories": "310 kcal",
        "img": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=500&auto=format&fit=crop&q=80"
    },
    "Butter Chicken": {
        "price": 380, "type": "Non-Veg",
        "desc": "Tandoori chicken pulled and simmered in velvet smooth tomato butter gravy.",
        "protein": "32g", "calories": "480 kcal",
        "img": "https://images.unsplash.com/photo-1603894584373-5ac82b6ae398?w=500&auto=format&fit=crop&q=80"
    },
    "Chicken Biryani": {
        "price": 320, "type": "Non-Veg",
        "desc": "Layers of long-grain aged basmati rice cooked with saffron and spiced meat.",
        "protein": "28g", "calories": "520 kcal",
        "img": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=500&auto=format&fit=crop&q=80"
    },
    "Gulab Jamun": {
        "price": 120, "type": "Veg",
        "desc": "Golden fried milk-solid spheres steeped gently in green cardamom sugar syrup.",
        "protein": "4g", "calories": "290 kcal",
        "img": "https://images.unsplash.com/photo-1593791330364-e8b4eeb6ceca?w=500&auto=format&fit=crop&q=80"
    }
}

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h2 style='text-align:center; color:#2563eb;'>📋 Operations Menu</h2>", unsafe_allow_html=True)
view_state = st.sidebar.radio("Navigate Workspace:",
                              ["🛒 Digital Front (Client)", "📊 Analytics Console (Admin)", "⭐ Feedback Hub"])

# ==========================================
# VIEW A: DIGITAL CLIENT FRONT
# ==========================================
if view_state == "🛒 Digital Front (Client)":
    st.markdown("<h1 class='main-header'>🍳 ZAIKA CLOUD KITCHEN</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Freshly Prepared Authentic Indian Delicacies Dispatched Instantly</p>",
                unsafe_allow_html=True)

    # Advanced Filters
    st.markdown("### 🔍 Filter Menu")
    f_col1, f_col2 = st.columns([1, 2])
    with f_col1:
        type_filter = st.radio("Diet Preference:", ["All Items", "Veg Only", "Non-Veg Only"])
    with f_col2:
        max_budget = st.slider("Budget Limit (₹):", min_value=100, max_value=500, value=500, step=10)

    st.markdown("---")

    # Displaying Items based on filters
    st.markdown("### 🍽️ Premium Menu")
    visible_items = {}
    for item, specs in menu.items():
        if specs['price'] <= max_budget:
            if type_filter == "Veg Only" and specs['type'] != "Veg": continue
            if type_filter == "Non-Veg Only" and specs['type'] != "Non-Veg": continue
            visible_items[item] = specs

    if visible_items:
        cols = st.columns(len(visible_items))
        for idx, (item, specs) in enumerate(visible_items.items()):
            with cols[idx]:
                st.markdown(f"""
                    <div class='food-card'>
                        <img src='{specs['img']}' style='width:100%; border-radius:8px; height:140px; object-fit:cover;'>
                        <h4 style='margin:10px 0 5px 0; color:#1e293b;'>{item} <span style='font-size:10px; color:{"#16a34a" if specs['type'] == "Veg" else "#dc2626"};'>● {specs['type']}</span></h4>
                        <p style='font-size:12px; color:#64748b; margin:0 0 10px 0; height:50px; overflow:hidden;'>{specs['desc']}</p>
                        <span class='macro-tag'>💪 Prot: {specs['protein']}</span>
                        <span class='macro-tag' style='background-color:#fff7ed; color:#c2410c;'>🔥 {specs['calories']}</span>
                        <h3 style='margin:10px 0 0 0; color:#2563eb;'>₹{specs['price']}</h3>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No items match your selected filters.")

    st.markdown("---")

    # Order Placement Form (With Animation)
    st.markdown("### 📝 Place Order")
    with st.form("transaction_entry_block", clear_on_submit=True):
        c_name = st.text_input("Customer Name:")
        c_dish = st.selectbox("Select Dish:", list(menu.keys()))
        c_qty = st.number_input("Quantity:", min_value=1, max_value=10, value=1, step=1)

        trigger_commit = st.form_submit_button("Place Order Now 🚀")

        if trigger_commit:
            if c_name.strip():
                final_cost = menu[c_dish]['price'] * c_qty
                record = {
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Customer Name': c_name, 'Dish': c_dish, 'Quantity': c_qty, 'Total Price': final_cost
                }

                # Order Processing Animation
                status_block = st.empty()
                progress_meter = st.progress(0)

                stages = [
                    ("Validating Order Details...", 20),
                    ("Order received by Kitchen - Chef Preparing...", 60),
                    ("Order Packed - Out for Delivery...", 100)
                ]
                for text, perc in stages:
                    status_block.info(f"⚡ Status: {text}")
                    progress_meter.progress(perc)
                    time.sleep(1)  # Delay for realistic feeling

                status_block.empty()
                progress_meter.empty()

                # Saving order
                pd_df = pd.read_csv(ORDER_FILE)
                pd_df = pd.concat([pd_df, pd.DataFrame([record])], ignore_index=True)
                pd_df.to_csv(ORDER_FILE, index=False)

                st.success(f"Order Successfully Placed! Total amount: ₹{final_cost}.")
                st.balloons()
            else:
                st.error("Please enter your name to place the order.")

# ==========================================
# VIEW B: ANALYTICS CONSOLE (ADMIN)
# ==========================================
elif view_state == "📊 Analytics Console (Admin)":
    st.title("📊 Kitchen Analytics & Sales Data")
    orders_df = pd.read_csv(ORDER_FILE)

    if not orders_df.empty:
        revenue_sum = orders_df['Total Price'].sum()
        total_count = len(orders_df)
        computed_aov = revenue_sum / total_count

        met_col1, met_col2, met_col3 = st.columns(3)
        with met_col1:
            st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
            st.metric("Total Revenue", f"₹{revenue_sum:,}")
            st.markdown("</div>", unsafe_allow_html=True)
        with met_col2:
            st.markdown("<div class='metric-container' style='border-left-color:#16a34a;'>", unsafe_allow_html=True)
            st.metric("Total Orders", f"{total_count} Orders")
            st.markdown("</div>", unsafe_allow_html=True)
        with met_col3:
            st.markdown("<div class='metric-container' style='border-left-color:#9333ea;'>", unsafe_allow_html=True)
            st.metric("Avg Order Value", f"₹{round(computed_aov, 2)}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.subheader("📈 Top Selling Items")
            item_aggregates = orders_df.groupby('Dish')['Quantity'].sum().reset_index()
            st.bar_chart(data=item_aggregates, x='Dish', y='Quantity', use_container_width=True)
        with v_col2:
            st.subheader("🕒 Sales Trend")
            st.line_chart(data=orders_df, x='Timestamp', y='Total Price', use_container_width=True)

        st.markdown("---")
        st.subheader("📜 Order Logs")
        st.dataframe(orders_df.sort_values(by='Timestamp', ascending=False), use_container_width=True, hide_index=True)
    else:
        st.info("No orders received yet.")

# ==========================================
# VIEW C: FEEDBACK HUB
# ==========================================
elif view_state == "⭐ Feedback Hub":
    st.title("⭐ Customer Reviews & Ratings")

    with st.form("feedback_entry_form", clear_on_submit=True):
        f_user = st.text_input("Your Name:")
        f_dish = st.selectbox("Dish you tried:", list(menu.keys()))
        f_stars = st.slider("Rating (Stars):", min_value=1, max_value=5, value=5)
        f_text = st.text_area("Your Review:")

        commit_review = st.form_submit_button("Submit Review 📝")
        if commit_review:
            if f_user.strip():
                review_rec = {
                    'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'User Name': f_user, 'Dish Sampled': f_dish, 'Stars': f_stars, 'Comments': f_text
                }
                rev_df = pd.read_csv(REVIEW_FILE)
                rev_df = pd.concat([rev_df, pd.DataFrame([review_rec])], ignore_index=True)
                rev_df.to_csv(REVIEW_FILE, index=False)
                st.success("Thank you for your feedback!")
            else:
                st.error("Please enter your name.")

    st.markdown("---")
    st.subheader("💬 Recent Customer Reviews")
    read_rev = pd.read_csv(REVIEW_FILE)
    if not read_rev.empty:
        for r_idx, r_row in read_rev.sort_values(by='Timestamp', ascending=False).iterrows():
            st.markdown(f"""
                <div style='background-color:#f1f5f9; padding:12px; border-radius:8px; margin-bottom:10px;'>
                    <b>{r_row['User Name']}</b> rated <span style='color:#2563eb;'>{r_row['Dish Sampled']}</span> — {'★' * int(r_row['Stars'])}{'☆' * (5 - int(r_row['Stars']))}
                    <p style='font-style:italic; margin:5px 0 0 0; font-size:13px; color:#475569;'>" {r_row['Comments']} "</p>
                    <span style='font-size:10px; color:#94a3b8;'>Posted on: {r_row['Timestamp']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No reviews yet. Be the first one to rate!")