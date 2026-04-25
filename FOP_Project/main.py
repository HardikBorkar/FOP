import streamlit as st
import ctypes

# Load DLL
lib = ctypes.CDLL("./logic.dll")

# ----------------- Fix ctypes argument types -----------------

# Addshelter
lib.addshelter.argtypes = [
    ctypes.c_int,        # id
    ctypes.c_char_p,     # name
    ctypes.c_char_p,     # location
    ctypes.c_int,        # capacity
    ctypes.c_int,        # food
    ctypes.c_int,        # water
    ctypes.c_int,        # med
    ctypes.c_int         # admitted
]
lib.addshelter.restype = ctypes.c_int

# Admit
lib.admit.argtypes = [ctypes.c_int, ctypes.c_int]
lib.admit.restype = ctypes.c_int

# Restock
lib.restock.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
lib.restock.restype = ctypes.c_int

# Transfer
lib.transfer.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
lib.transfer.restype = ctypes.c_int

# Shortage
lib.shortage.argtypes = []
lib.shortage.restype = ctypes.c_int

# ---------------- Streamlit Page Config ----------------
st.set_page_config(
    page_title="Disaster Resource Manager",
    page_icon="🚑",
    layout="wide"
)

st.title("🚑 Disaster Resource Management System")
st.markdown("### 🏥 Manage shelters, resources, and emergencies efficiently")
st.divider()

# Sidebar menu
st.sidebar.title("📋 Menu")
choice = st.sidebar.radio(
    "Select Operation",
    [
        "➕ Add Shelter",
        "📄 View Shelters",
        "🏠 Admit People",
        "⚠️ Check Shortage",
        "📦 Restock Resources",
        "🔄 Transfer Resources"
    ]
)

# ---------------- ADD SHELTER ----------------
if choice == "➕ Add Shelter":
    st.header("➕ Add New Shelter")

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            sid = st.number_input("🆔 Shelter ID", step=1)
            name = st.text_input("🏷️ Shelter Name")
            location = st.text_input("📍 Location")
            admitted = st.number_input("👤 Admitted People", step=1, min_value=0)

        with col2:
            capacity = st.number_input("👥 Capacity", step=1)
            food = st.number_input("🍞 Food Units", step=1)
            water = st.number_input("💧 Water Units", step=1)
            med = st.number_input("💊 Medical Kits", step=1)

    if st.button("✅ Add Shelter"):
        ret = lib.addshelter(
            ctypes.c_int(sid),
            ctypes.c_char_p(name.encode('utf-8')),
            ctypes.c_char_p(location.encode('utf-8')),
            ctypes.c_int(capacity),
            ctypes.c_int(food),
            ctypes.c_int(water),
            ctypes.c_int(med),
            ctypes.c_int(admitted)
        )
        if ret == 1:
            st.success("🎉 Shelter added successfully!")
        else:
            st.error("❌ Failed to add shelter!")

# ---------------- VIEW SHELTERS ----------------
elif choice=="📄 View Shelters":
    st.header("📄 All Registered Shelters")
    st.info("ℹ️ Below are all shelters stored in the system:")

    try:
        with open("Shelter.txt", "r") as f:
            shelters = f.readlines()
        
        if not shelters:
            st.warning("⚠️ No shelters found!")
        else:
            for line in shelters:
                fields = line.strip().split("||")
                if len(fields) == 8:
                    st.markdown(
                        f"**🆔 Shelter ID:** {fields[0]}\t||\t\t"
                        f"🏷️ **Name:** {fields[1]}\t\t||\t\t"
                        f"📍 **Location:** {fields[2]}\t\t||\t\t"
                        f"👥 **Capacity:** {fields[3]}\n\n"
                        f"🏠 **Admitted:** {fields[7]}\t\t||\t\t"
                        f"🍞 **Food Units:** {fields[4]}\t\t||\t\t"
                        f"💧 **Water Units:** {fields[5]}\t\t||\t\t"
                        f"💊 **Medical Kits:** {fields[6]}\n\n"
                        f"---"
                    )
    except FileNotFoundError:
        st.warning("⚠️ Shelter records not found!")

# ---------------- ADMIT ----------------
elif choice=="🏠 Admit People":
    st.subheader("🚪 Admit People")

    sid = st.number_input("Enter Shelter ID", step=1)
    count = st.number_input("👨‍👩‍👧‍👦 People to Admit", min_value=1, step=1)

    if st.button("🚪 Admit"):

        found = False
        shortage_flag = False

        try:
            with open("Shelter.txt", "r") as f:
                for line in f:
                    parts = line.strip().split("||")
                    if len(parts) != 8:
                        continue

                    file_sid = int(parts[0])
                    cap  = int(parts[3])
                    food = int(parts[4])
                    water= int(parts[5])
                    med  = int(parts[6])
                    already_admitted = int(parts[7])

                    if file_sid == sid:
                        found = True

                        
                        new_total_people = already_admitted + count

                        
                        if new_total_people > cap:
                            st.error("⚠️ Not enough capacity in shelter!")
                            shortage_flag = True
                            break

                        
                        required_food  = new_total_people * 2
                        required_water = new_total_people * 3
                        required_med   = new_total_people * 1

                        
                        food_short  = max(0, required_food  - food)
                        water_short = max(0, required_water - water)
                        med_short   = max(0, required_med   - med)

                        if food_short > 0 or water_short > 0 or med_short > 0:
                            st.error("🛑 Admission would cause RESOURCE SHORTAGE!")

                            if food_short > 0:
                                st.warning(f"🍞 Food shortage after admit: {food_short}")

                            if water_short > 0:
                                st.warning(f"💧 Water shortage after admit: {water_short}")

                            if med_short > 0:
                                st.warning(f"💊 Medicine shortage after admit: {med_short}")

                            shortage_flag = True
                            break

            if not found:
                st.error("❌ Shelter not found!")

            elif not shortage_flag:
                
                ret = lib.admit(ctypes.c_int(sid), ctypes.c_int(count))

                if ret == 1:
                    st.success("🎉 People admitted successfully!")
                else:
                    st.error("❌ Admission failed!")

        except FileNotFoundError:
            st.error("Shelter.txt not found!")

#---------------SHORTAGES--------------
elif choice == "⚠️ Check Shortage":
    
    st.header("⚠️ Resource Shortage Alert")

    if st.button("🔍 Check Now"):
        
        count = 0
        shortages = []

        try:
            with open("Shelter.txt", "r") as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split("||")

                    if len(parts) != 8:
                        continue  

                    sid = int(parts[0])
                    name = parts[1]
                    location = parts[2]
                    cap = int(parts[3])
                    food = int(parts[4])
                    water = int(parts[5])
                    med = int(parts[6])
                    ad = int(parts[7])

                    
                    f_short = 0
                    w_short = 0
                    m_short = 0

                    if food < cap * 2:
                        f_short = (cap * 2) - food

                    if water < cap * 3:
                        w_short = (cap * 3) - water

                    if med < cap:
                        m_short = cap - med

                    if f_short > 0 or w_short > 0 or m_short > 0:
                        shortages.append({
                            "id": sid,
                            "food": f_short,
                            "water": w_short,
                            "med": m_short
                        })
                        count += 1

        except FileNotFoundError:
            st.error("🚫 Shelter.txt file not found!")
            st.stop()

        # ---- DISPLAY SECTION ----
        
        if count == 0:
            st.success("✅ All shelters have sufficient resources!")
        else:
            st.warning(f"🚨 {count} shelter(s) have shortages!")

            for item in shortages:

                message = f"🏠 Shelter ID: {item['id']}\n"

                if item["food"] > 0:
                    message += f"🍞 Food shortage: {item['food']} units\n"

                if item["water"] > 0:
                    message += f"💧 Water shortage: {item['water']} units\n"

                if item["med"] > 0:
                    message += f"💊 Medicine shortage: {item['med']} kits\n"

                st.error(message)
# ---------------- RESTOCK ----------------
elif choice == "📦 Restock Resources":
    st.header("📦 Restock Shelter Resources")

    sid = st.number_input("🆔 Shelter ID", step=1)

    col1, col2, col3 = st.columns(3)

    with col1:
        food = st.number_input("🍞 Add Food", step=1)
    with col2:
        water = st.number_input("💧 Add Water", step=1)
    with col3:
        med = st.number_input("💊 Add Medical Kits", step=1)

    if st.button("🔄 Restock"):
        ret = lib.restock(ctypes.c_int(sid), ctypes.c_int(food), ctypes.c_int(water), ctypes.c_int(med))
        if ret == 1:
            st.success("🎉 Resources updated successfully!")
        else:
            st.error("❌ Shelter not found!")

# ---------------- TRANSFER ----------------
elif choice == "🔄 Transfer Resources":
    st.header("🔄 Transfer Resources Between Shelters")

    col1, col2 = st.columns(2)

    with col1:
        from_id = st.number_input("🏠 From Shelter ID", step=1)
    with col2:
        to_id = st.number_input("🏠 To Shelter ID", step=1)

    resource = st.selectbox(
        "📦 Select Resource",
        ["🍞 Food", "💧 Water", "💊 Medical"]
    )

    amount = st.number_input("🔢 Amount to Transfer", step=1)

    if st.button("🚚 Transfer"):
        food = water = med = 0
        if resource == "🍞 Food":
            food = amount
        elif resource == "💧 Water":
            water = amount
        else:
            med = amount

        ret = lib.transfer(
            ctypes.c_int(from_id),
            ctypes.c_int(to_id),
            ctypes.c_int(food),
            ctypes.c_int(water),
            ctypes.c_int(med)
        )
        if ret == 1:
            st.success("✅ Transfer completed successfully!")
        else:
            st.error("❌ Transfer failed!")

st.divider()
st.markdown("### 💡 Stay Prepared. Stay Safe.")