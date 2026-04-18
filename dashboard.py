import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

st.set_page_config(page_title="OmniPrice", page_icon="💰", layout="wide")
st.title("💰 OmniPrice Dashboard")
st.caption("Automated Market Intelligence & Price Analytics")

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("Actions")
page = st.sidebar.radio("Navigate", ["Price Monitor", "Stores", "Products", "Add Competitor Link"])

# ── Helpers ────────────────────────────────────────────────────────────────────

def get(path):
    try:
        r = requests.get(f"{API}{path}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return []


def post(path, data):
    try:
        r = requests.post(f"{API}{path}", json=data)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None

# ── Price Monitor ──────────────────────────────────────────────────────────────

if page == "Price Monitor":
    st.header("Price Monitor")

    products = get("/api/products/")
    if not products:
        st.info("No products yet. Add one in the Products tab.")
        st.stop()

    product_map = {p["name"]: p["id"] for p in products}
    selected = st.selectbox("Select a product", list(product_map.keys()))
    product_id = product_map[selected]

    links = get(f"/api/competitor-links/?product_id={product_id}")
    if not links:
        st.info("No competitor links for this product yet.")
        st.stop()

    stores = {s["id"]: s["name"] for s in get("/api/stores/")}

    st.subheader("Latest Prices")
    rows = []
    for link in links:
        logs = get(f"/api/price-logs/?competitor_link_id={link['id']}")
        if logs:
            latest = logs[0]
            rows.append({
                "Store": stores.get(link["store_id"], "Unknown"),
                "Price (ISK)": f"{latest['price']:,.0f}",
                "In Stock": "✅" if latest["in_stock"] else "❌",
                "Last Scraped": latest["scraped_at"][:16].replace("T", " "),
                "URL": link["url"],
            })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Scrape button
        st.subheader("Run Scrape")
        if st.button("🔄 Scrape All Competitor Links Now"):
            for link in links:
                with st.spinner(f"Scraping {link['url']}..."):
                    result = post(f"/api/scrape/{link['id']}", {})
                    if result:
                        st.success(f"Got price: {result['price']:,.0f} ISK from {stores.get(link['store_id'], 'Unknown')}")
            st.rerun()
    else:
        st.info("No price data yet. Run a scrape first.")
        if st.button("🔄 Scrape Now"):
            for link in links:
                with st.spinner(f"Scraping..."):
                    post(f"/api/scrape/{link['id']}", {})
            st.rerun()

    # Price history chart
    st.subheader("Price History")
    history_rows = []
    for link in links:
        logs = get(f"/api/price-logs/?competitor_link_id={link['id']}")
        for log in logs:
            history_rows.append({
                "Store": stores.get(link["store_id"], "Unknown"),
                "Price": log["price"],
                "Date": log["scraped_at"][:10],
            })

    if history_rows:
        hist_df = pd.DataFrame(history_rows)
        pivot = hist_df.pivot_table(index="Date", columns="Store", values="Price", aggfunc="mean")
        st.line_chart(pivot)

# ── Stores ─────────────────────────────────────────────────────────────────────

elif page == "Stores":
    st.header("Stores")

    stores = get("/api/stores/")
    if stores:
        st.dataframe(pd.DataFrame(stores)[["id", "name", "base_url", "currency"]], use_container_width=True, hide_index=True)
    else:
        st.info("No stores yet.")

    st.subheader("Add Store")
    with st.form("add_store"):
        name = st.text_input("Store Name", placeholder="Elko")
        base_url = st.text_input("Base URL", placeholder="https://www.elko.is")
        currency = st.selectbox("Currency", ["ISK", "USD", "EUR", "GBP"])
        if st.form_submit_button("Add Store"):
            result = post("/api/stores/", {"name": name, "base_url": base_url, "currency": currency})
            if result:
                st.success(f"Store '{name}' added!")
                st.rerun()

# ── Products ───────────────────────────────────────────────────────────────────

elif page == "Products":
    st.header("Products")

    products = get("/api/products/")
    if products:
        st.dataframe(pd.DataFrame(products)[["id", "name", "sku", "category"]], use_container_width=True, hide_index=True)
    else:
        st.info("No products yet.")

    st.subheader("Add Product")
    with st.form("add_product"):
        name = st.text_input("Product Name", placeholder="iPhone 16")
        sku = st.text_input("SKU", placeholder="IPH16-128")
        category = st.text_input("Category", placeholder="Electronics")
        if st.form_submit_button("Add Product"):
            result = post("/api/products/", {"name": name, "sku": sku, "category": category})
            if result:
                st.success(f"Product '{name}' added!")
                st.rerun()

# ── Add Competitor Link ────────────────────────────────────────────────────────

elif page == "Add Competitor Link":
    st.header("Add Competitor Link")
    st.caption("Link a product to a competitor's product page URL")

    products = get("/api/products/")
    stores = get("/api/stores/")

    if not products or not stores:
        st.warning("You need at least one product and one store first.")
        st.stop()

    product_map = {p["name"]: p["id"] for p in products}
    store_map = {s["name"]: s["id"] for s in stores}

    with st.form("add_link"):
        product = st.selectbox("Product", list(product_map.keys()))
        store = st.selectbox("Store", list(store_map.keys()))
        url = st.text_input("Competitor Product URL", placeholder="https://www.elko.is/vorur/apple-iphone-16/...")
        if st.form_submit_button("Add Link"):
            result = post("/api/competitor-links/", {
                "product_id": product_map[product],
                "store_id": store_map[store],
                "url": url,
            })
            if result:
                st.success("Competitor link added!")
                st.rerun()

    st.subheader("Existing Links")
    links = get("/api/competitor-links/")
    if links:
        rows = []
        for link in links:
            product_name = next((p["name"] for p in products if p["id"] == link["product_id"]), "Unknown")
            store_name = next((s["name"] for s in stores if s["id"] == link["store_id"]), "Unknown")
            rows.append({"ID": link["id"], "Product": product_name, "Store": store_name, "URL": link["url"]})
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
