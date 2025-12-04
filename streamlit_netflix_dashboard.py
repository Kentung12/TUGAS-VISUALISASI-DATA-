import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================
# 1) PENGATURAN HALAMAN
# =========================================================
st.set_page_config(
    layout="wide",
    page_title="Dashboard Netflix Top10",
    page_icon="🎬",
)

DATA_PATH = "netflix_cleaned_sample.csv"
TOP_N = 10  # hanya untuk BAR & LINE

# =========================================================
# 2) PILIH TEMA (GELAP / TERANG) 
# =========================================================
st.sidebar.header("Tampilan")
mode_terang = st.sidebar.toggle("🌞 Mode Terang", value=False)


def rgba_tuple(r, g, b, a):
    return (r / 255, g / 255, b / 255, a)


if mode_terang:
    TOK = {
        "bg": "#F6F7FB",
        "panel": "rgba(0,0,0,0.04)",
        "panel2": "rgba(0,0,0,0.06)",
        "stroke": "rgba(0,0,0,0.10)",
        "text": "#0F172A",
        "muted": "rgba(15,23,42,0.62)",
        "chip": "rgba(229,9,20,0.10)",
        "sidebar": "rgba(0,0,0,0.02)",
        "centre": "#F6F7FB",
        # Matplotlib
        "mpl_text": "#0F172A",
        "mpl_tick": "#0F172A",
        "mpl_edge": rgba_tuple(15, 23, 42, 0.25),
        "mpl_grid": rgba_tuple(15, 23, 42, 0.12),
        "mpl_axes_bg": "#FFFFFF",
    }
else:
    TOK = {
        "bg": "#0B0B0F",
        "panel": "rgba(255,255,255,0.06)",
        "panel2": "rgba(255,255,255,0.08)",
        "stroke": "rgba(255,255,255,0.12)",
        "text": "#EDEDED",
        "muted": "rgba(237,237,237,0.70)",
        "chip": "rgba(229,9,20,0.16)",
        "sidebar": "rgba(255,255,255,0.04)",
        "centre": "#0B0B0F",
        # Matplotlib
        "mpl_text": "#EDEDED",
        "mpl_tick": "#CFCFCF",
        "mpl_edge": rgba_tuple(255, 255, 255, 0.16),
        "mpl_grid": rgba_tuple(255, 255, 255, 0.12),
        "mpl_axes_bg": "#0B0B0F",
    }

# Terapkan style ke Matplotlib (grafik)
plt.rcParams.update(
    {
        "figure.facecolor": "none",
        "axes.facecolor": TOK["mpl_axes_bg"],
        "axes.edgecolor": TOK["mpl_edge"],
        "axes.labelcolor": TOK["mpl_text"],
        "xtick.color": TOK["mpl_tick"],
        "ytick.color": TOK["mpl_tick"],
        "text.color": TOK["mpl_text"],
        "grid.color": TOK["mpl_grid"],
        "axes.titleweight": "bold",
        "font.size": 11,
    }
)
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=["#E50914", "#B20710", "#64748B", "#111827"])

# CSS untuk mempercantik tampilan Streamlit 
st.markdown(
    f"""
    <style>
      :root {{
        --bg: {TOK["bg"]};
        --panel: {TOK["panel"]};
        --panel2: {TOK["panel2"]};
        --stroke: {TOK["stroke"]};
        --text: {TOK["text"]};
        --muted: {TOK["muted"]};
        --chip: {TOK["chip"]};
      }}

      html, body, [class*="st-"], .stMarkdown, .stText, p, span, div, h1, h2, h3, h4, h5, h6 {{
        font-style: normal !important;
      }}

      .stApp {{
        background:
          radial-gradient(1100px 650px at 10% -12%, rgba(229,9,20,{0.16 if mode_terang else 0.26}), transparent 60%),
          radial-gradient(900px 600px at 92% -5%, rgba(178,7,16,{0.10 if mode_terang else 0.20}), transparent 55%),
          var(--bg);
      }}

      [data-testid="stSidebar"] {{
        background: {TOK["sidebar"]};
        border-right: 1px solid var(--stroke);
      }}

      .panel {{
        border: 1px solid var(--stroke);
        background: var(--panel);
        border-radius: 18px;
        padding: 14px;
      }}

      .topbar {{
        border: 1px solid var(--stroke);
        background: linear-gradient(135deg, rgba(229,9,20,{0.10 if mode_terang else 0.14}), var(--panel));
        border-radius: 18px;
        padding: 16px 18px;
      }}

      .chip {{
        display:inline-flex;
        align-items:center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: var(--chip);
        border: 1px solid var(--stroke);
        color: var(--text);
        font-size: .92rem;
        white-space: nowrap;
      }}

      .muted {{
        color: var(--muted);
        font-size: .95rem;
      }}

      [data-testid="stMetric"] {{
        background: var(--panel2);
        border: 1px solid var(--stroke);
        padding: 12px 12px 10px 12px;
        border-radius: 16px;
      }}

      .stDataFrame {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid var(--stroke);
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 3) LOAD DATA
# =========================================================
if not os.path.exists(DATA_PATH):
    st.error(f"❌ File '{DATA_PATH}' tidak ditemukan. Pastikan file berada di folder yang sama.")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["week"] = pd.to_datetime(df["week"], errors="coerce")
if "title" not in df.columns and "show_title" in df.columns:
    df["title"] = df["show_title"]

# =========================================================
# 4) FILTER 
# =========================================================
st.sidebar.header("Filter Data")

kategori = ["Semua"] + sorted(df["category"].dropna().unique().tolist())
pilih_kategori = st.sidebar.selectbox("Pilih Kategori", kategori)

min_week = df["week"].min().to_pydatetime()
max_week = df["week"].max().to_pydatetime()
rentang_minggu = st.sidebar.slider(
    "Rentang Minggu",
    min_value=min_week,
    max_value=max_week,
    value=(min_week, max_week),
    format="YYYY-MM-DD",
)

filtered = df.copy()
if pilih_kategori != "Semua":
    filtered = filtered[filtered["category"] == pilih_kategori]
filtered = filtered[(filtered["week"] >= rentang_minggu[0]) & (filtered["week"] <= rentang_minggu[1])]

# =========================================================
# 5) KPI
# =========================================================
baris_data = len(filtered)

hours_series = (
    pd.to_numeric(filtered["weekly_hours_viewed"], errors="coerce")
    if ("weekly_hours_viewed" in filtered.columns and baris_data > 0)
    else pd.Series(dtype="float64")
)

total_jam = float(hours_series.sum()) if not hours_series.empty else 0.0
puncak_jam = float(hours_series.max()) if not hours_series.empty else 0.0
avg_jam = float(hours_series.mean()) if not hours_series.empty else 0.0

# =========================================================
# 6) HEADER (TOPBAR)
# =========================================================
chip_text = f"{pilih_kategori} • {rentang_minggu[0].date()} → {rentang_minggu[1].date()}"
st.markdown(
    f"""
    <div class="topbar">
      <h2 style="margin:0; color:{TOK["text"]}">🎬 Dashboard Netflix Top 10</h2>
      <div class="muted">Analisis performa film/series berdasarkan jam tayang mingguan Top 10 global</div>
      <div style="margin-top:10px;" class="chip">🔎 Filter aktif: {chip_text}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

# KPI row (4 item)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Baris Data", f"{baris_data:,}")
with k2:
    st.metric("Total Jam Tayang", f"{total_jam:,.0f}")
with k3:
    st.metric("Puncak Jam Tayang", f"{puncak_jam:,.0f}")
with k4:
    st.metric("Rata-rata Jam Tayang", f"{avg_jam:,.0f}")

st.write("")

# =========================================================
# 7) TAB
# =========================================================
tab1, tab2 = st.tabs(["📊 Grafik", "📄 Data"])


def style_axes(ax):
    ax.grid(True, axis="y", linestyle="-", linewidth=0.6, alpha=0.80)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


with tab1:
    st.markdown("### 📊 Grafik Utama")

    col1, col2 = st.columns(2)

    # 1) BAR CHART — tampilkan 10 judul saja 
    with col1:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Top 10 Tayangan (Jam Tayang Mingguan Tertinggi)")

        if baris_data == 0:
            st.info("Tidak ada data pada filter yang dipilih.")
        elif "weekly_hours_viewed" not in filtered.columns:
            st.info("Kolom weekly_hours_viewed tidak ditemukan.")
        else:
            top10 = (
                pd.to_numeric(filtered["weekly_hours_viewed"], errors="coerce")
                .groupby(filtered["title"])
                .max()
                .nlargest(TOP_N)
            )

            fig, ax = plt.subplots(figsize=(7.2, 4.3))
            ax.bar(top10.index.astype(str), top10.values)
            ax.set_ylabel("Jam Tayang Mingguan (Max)")
            ax.set_xlabel("Judul")
            ax.tick_params(axis="x", rotation=55)
            style_axes(ax)
            st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 2) LINE CHART — tampilkan 10 judul saja
    with col2:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Total Jam Tayang per Judul (Akumulasi - Top 10)")

        if baris_data == 0:
            st.info("Tidak ada data pada filter yang dipilih.")
        elif "weekly_hours_viewed" not in filtered.columns:
            st.info("Kolom weekly_hours_viewed tidak ditemukan.")
        else:
            top_titles = (
                pd.to_numeric(filtered["weekly_hours_viewed"], errors="coerce")
                .groupby(filtered["title"])
                .max()
                .nlargest(TOP_N)
                .index
            )

            title_sum = (
                pd.to_numeric(filtered["weekly_hours_viewed"], errors="coerce")
                .groupby(filtered["title"])
                .sum()
                .reindex(top_titles)
            )

            fig, ax = plt.subplots(figsize=(7.2, 4.3))
            ax.plot(title_sum.index.astype(str), title_sum.values, linewidth=2.2, marker="o")
            ax.fill_between(range(len(title_sum.values)), title_sum.values, alpha=0.12)
            ax.set_xlabel("Judul")
            ax.set_ylabel("Total Jam Tayang")
            ax.tick_params(axis="x", rotation=55)
            style_axes(ax)
            st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    col3, col4 = st.columns(2)

    # 3) DONUT — 
    with col3:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Distribusi Kategori")

        if baris_data == 0:
            st.info("Tidak ada data pada filter yang dipilih.")
        else:
            cat_count = filtered["category"].value_counts()
            fig, ax = plt.subplots(figsize=(7.2, 5.2))
            ax.pie(
                cat_count.values,
                labels=cat_count.index.astype(str),
                autopct="%1.1f%%",
                startangle=90,
                pctdistance=0.82,
                textprops={"color": TOK["text"]},
            )
            centre = plt.Circle((0, 0), 0.66, fc=TOK["centre"])
            fig.gca().add_artist(centre)
            ax.set_aspect("equal")
            st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # 4) SCATTER —
    with col4:
        st.markdown("<div class='panel'>", unsafe_allow_html=True)
        st.subheader("Runtime vs Jam Tayang Mingguan")

        if baris_data == 0 or "runtime" not in filtered.columns:
            st.info("Tidak ada data/kolom runtime pada filter yang dipilih.")
        else:
            x = pd.to_numeric(filtered["runtime"], errors="coerce")
            y = pd.to_numeric(filtered["weekly_hours_viewed"], errors="coerce") if "weekly_hours_viewed" in filtered.columns else None

            if y is None:
                st.info("Kolom weekly_hours_viewed tidak ditemukan.")
            else:
                mask = ~(x.isna() | y.isna())
                fig, ax = plt.subplots(figsize=(7.2, 5.2))
                ax.scatter(x[mask], y[mask], alpha=0.35, s=28)
                ax.set_xlabel("Runtime (menit)")
                ax.set_ylabel("Jam Tayang Mingguan")
                style_axes(ax)
                st.pyplot(fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # 5) HEATMAP — tampilkan semua
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("🔥 Matriks Korelasi (Kolom Numerik)")

    num_df = filtered.select_dtypes(include="number")
    if num_df.shape[1] < 2:
        st.info("Kolom numerik tidak cukup untuk membuat korelasi (butuh minimal 2 kolom numerik).")
    else:
        fig, ax = plt.subplots(figsize=(10, 5.4))
        sns.heatmap(num_df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax, fmt=".2f")
        st.pyplot(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("### 📄 Data Hasil Filter")

    d1, d2 = st.columns([1, 2.2])
    with d1:
        st.download_button(
            "⬇️ Download CSV (filtered)",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="netflix_top10_filtered.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with d2:
        st.markdown(
            f"<div class='muted'>Menampilkan <b>{len(filtered):,}</b> baris • "
            f"Kategori: <b>{pilih_kategori}</b> • Rentang: <b>{rentang_minggu[0].date()}</b> s/d <b>{rentang_minggu[1].date()}</b></div>",
            unsafe_allow_html=True,
        )

    view_df = filtered.copy()
    if "weekly_hours_viewed" in view_df.columns:
        view_df["weekly_hours_viewed"] = pd.to_numeric(view_df["weekly_hours_viewed"], errors="coerce")

    styler = view_df.style
    if "weekly_hours_viewed" in view_df.columns:
        styler = styler.format({"weekly_hours_viewed": "{:,.0f}"})
    if "runtime" in view_df.columns:
        styler = styler.format({"runtime": "{:,.0f}"})

    st.dataframe(styler, use_container_width=True, height=520)

# =========================================================
# 8) CATATAN
# =========================================================
st.markdown("---")
st.caption("Catatan: Dataset telah melalui tahap pembersihan dan standarisasi kolom untuk memudahkan analisis.")

