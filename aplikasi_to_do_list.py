import streamlit as st
from datetime import datetime

# Konfigurasi 
st.set_page_config(page_title="To-Do List", page_icon="✅")

# Inisialisasi session state
if 'tugas' not in st.session_state:
    st.session_state.tugas = []

if 'hitung_tugas' not in st.session_state:
    st.session_state.hitung_tugas = 0

# Fungsi untuk menambahkan tugas
def tambah_tugas(text_tugas, prioritas):
    if text_tugas.strip():
        st.session_state.hitung_tugas += 1 
        tugas_baru = {
            "id_tugas" : st.session_state.hitung_tugas,
            "text" : text_tugas,
            "selesai" : False,
            "prioritas" : prioritas,
            "waktu_dibuat" : datetime.now().strftime("%d-%m-%y %H:%M")
        }
        st.session_state.tugas.append(tugas_baru)
        return True
    return False 

# Fungsi untuk toggle status tugas
def toggle_tugas(id_tugas):
    for tugas in st.session_state.tugas:
        if tugas['id_tugas'] == id_tugas:
            tugas['selesai'] = not tugas['selesai']
            break

# Fungsi untuk hapus task
def hapus_tugas(id_tugas):
    st.session_state.tugas = [t for t in st.session_state.tugas if t['id_tugas'] != id_tugas]

# Judul
col1, col2, col3 = st.columns([1,4,1])
with col2: 
    st.title("Aplikasi To-Do List")

# Form input
with st.form("form_tambah_tugas", clear_on_submit=True):
    col1, col2 = st.columns([3, 1])
    with col1:
        tugas_baru = st.text_input("Tugas baru", placeholder="Masukkan tugas Anda...")
    with col2:
        prioritas = st.selectbox("Prioritas", ["Rendah", "Sedang", "Tinggi"])
    
    submitted = st.form_submit_button("➕ Tambah Tugas", use_container_width=True)

    if submitted:
        if tambah_tugas(tugas_baru, prioritas):
            st.success("Tugas berhasil ditambahkan!")
        else:
            st.error("Tugas tidak boleh kosong!")

st.divider()

# Statistik
col1, col2, col3 = st.columns(3)
with col1:
    total_tugas = len(st.session_state.tugas)
    st.metric("TOTAL TUGAS", total_tugas)
with col2:
    tugas_selesai = len([t for t in st.session_state.tugas if t['selesai']])
    st.metric("SELESAI", tugas_selesai)
with col3:
    tugas_belum_selesai = total_tugas - tugas_selesai
    st.metric("BELUM SELESAI", tugas_belum_selesai)

# Filter
filter_tugas = st.radio(
    "Tampilkan:",
    ["Semua", "Belum Selesai", "Selesai"],
    horizontal=True
)

st.divider()

# Tampilkan daftar tugas
if st.session_state.tugas:
    tugas_terfilter = st.session_state.tugas

    if filter_tugas == "Belum Selesai":
        tugas_terfilter = [t for t in st.session_state.tugas if not t['selesai']]
    elif filter_tugas == "Selesai":
        tugas_terfilter = [t for t in st.session_state.tugas if t['selesai']]

    emoji_prioritas = {
        "Tinggi": "🔴",
        "Sedang": "🟡",
        "Rendah": "🟢"
    }

    for tugas in tugas_terfilter:

        col1, col2, col3 = st.columns([0.5, 3, 0.5])

        with col1:
            checked = st.checkbox(
                "✓",
                value=tugas['selesai'],
                key=f"check_{tugas['id_tugas']}"
            )
            if checked != tugas['selesai']:
                toggle_tugas(tugas['id_tugas'])
                st.rerun()

        with col2:
            tugas_style = "text-decoration: line-through; color: gray;" if tugas['selesai'] else ""
            st.markdown(
                f"<p style='{tugas_style}'>{emoji_prioritas[tugas['prioritas']]} {tugas['text']}<br>"
                f"<small style='color: gray;'>Dibuat: {tugas['waktu_dibuat']}</small></p>",
                unsafe_allow_html=True
            )

        with col3:
            if st.button("🗑️", key=f"del_{tugas['id_tugas']}", help="Hapus tugas"):
                hapus_tugas(tugas['id_tugas'])
                st.rerun()

        st.divider()

    # Hapus semua selesai
    if tugas_selesai > 0:
        if st.button("🧹 Hapus Semua Tugas Selesai"):
            st.session_state.tugas = [t for t in st.session_state.tugas if not t['selesai']]
            st.rerun()
else:
    st.info("👋 Belum ada tugas. Tambahkan tugas pertama Anda!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>TUGAS UAS PEMROGRAMAN DASAR</p>",
    unsafe_allow_html=True
)
