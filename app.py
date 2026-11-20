import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# ─────────────────────────────────────────────
#  KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard KPI KIKHB | PMS",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  TEMA WARNA: BIRU KORPORAT & EMAS
# ─────────────────────────────────────────────
BIRU_GELAP   = "#0D2B55"   # navy/korporat
BIRU_SEDANG  = "#1A4A8A"   # biru utama
BIRU_CERAH   = "#2E6EC4"   # biru highlight
BIRU_LEMBUT  = "#D6E4F7"   # biru latar
EMAS         = "#C9960C"   # emas korporat
EMAS_CERAH   = "#F0C040"   # emas terang
EMAS_LEMBUT  = "#FFF8E1"   # emas latar
HIJAU        = "#2E7D32"
HIJAU_LEMBUT = "#E8F5E9"
MERAH        = "#C62828"
MERAH_LEMBUT = "#FFEBEE"
KELABU       = "#607D8B"
PUTIH        = "#FFFFFF"

CUSTOM_CSS = f"""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Inter', sans-serif;
      background-color: #F0F4FA;
  }}

  /* ── Header utama ── */
  .main-header {{
      background: linear-gradient(135deg, {BIRU_GELAP} 0%, {BIRU_SEDANG} 60%, {BIRU_CERAH} 100%);
      padding: 24px 32px 20px 32px;
      border-radius: 12px;
      margin-bottom: 20px;
      border-bottom: 4px solid {EMAS};
      box-shadow: 0 4px 18px rgba(13,43,85,0.18);
  }}
  .main-header h1 {{
      color: {EMAS_CERAH};
      font-size: 1.9rem;
      font-weight: 800;
      margin: 0 0 4px 0;
      letter-spacing: 0.5px;
  }}
  .main-header p {{
      color: #B8D0F0;
      font-size: 0.9rem;
      margin: 0;
  }}

  /* ── Banner amaran ── */
  .banner-aktif {{
      background: linear-gradient(90deg, {BIRU_GELAP}, {BIRU_SEDANG});
      border-left: 6px solid {EMAS};
      color: white;
      padding: 14px 20px;
      border-radius: 8px;
      margin-bottom: 10px;
      font-size: 0.95rem;
      box-shadow: 0 2px 10px rgba(13,43,85,0.15);
  }}
  .banner-akan-datang {{
      background: linear-gradient(90deg, {EMAS} 0%, #A67800 100%);
      border-left: 6px solid {EMAS_CERAH};
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      margin-bottom: 20px;
      font-size: 0.88rem;
      box-shadow: 0 2px 8px rgba(201,150,12,0.18);
  }}

  /* ── KPI Cards ── */
  .kpi-card {{
      background: {PUTIH};
      border-radius: 12px;
      padding: 20px 22px;
      border-top: 4px solid {BIRU_CERAH};
      box-shadow: 0 2px 10px rgba(0,0,0,0.07);
      text-align: center;
      height: 140px;
      display: flex;
      flex-direction: column;
      justify-content: center;
  }}
  .kpi-card .kpi-label {{
      font-size: 0.78rem;
      color: {KELABU};
      text-transform: uppercase;
      letter-spacing: 0.8px;
      font-weight: 600;
      margin-bottom: 8px;
  }}
  .kpi-card .kpi-value {{
      font-size: 2rem;
      font-weight: 800;
      color: {BIRU_GELAP};
      line-height: 1;
  }}
  .kpi-card .kpi-sub {{
      font-size: 0.75rem;
      color: {KELABU};
      margin-top: 5px;
  }}
  .kpi-card-emas {{
      border-top-color: {EMAS};
  }}
  .kpi-card-hijau {{
      border-top-color: {HIJAU};
  }}
  .kpi-card .kpi-value-hijau {{ color: {HIJAU}; }}
  .kpi-card .kpi-value-emas  {{ color: {EMAS};  }}

  /* ── Timeline cards ── */
  .timeline-wrap {{
      display: flex;
      gap: 10px;
      flex-wrap: nowrap;
      overflow-x: auto;
      padding-bottom: 8px;
      margin-bottom: 20px;
  }}
  .tl-card {{
      min-width: 110px;
      flex: 1;
      border-radius: 10px;
      padding: 14px 10px;
      text-align: center;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: default;
      border: 2px solid transparent;
      box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }}
  .tl-selesai  {{ background:{HIJAU_LEMBUT}; border-color:{HIJAU};  color:{HIJAU};  }}
  .tl-aktif    {{ background:{BIRU_LEMBUT};  border-color:{BIRU_CERAH}; color:{BIRU_GELAP}; }}
  .tl-akan     {{ background:#F5F5F5;        border-color:#BDBDBD;  color:{KELABU};  }}
  .tl-badge {{
      display: inline-block;
      padding: 2px 10px;
      border-radius: 20px;
      font-size: 0.7rem;
      font-weight: 700;
      margin-top: 6px;
  }}
  .badge-selesai {{ background:{HIJAU};     color:white; }}
  .badge-aktif   {{ background:{BIRU_CERAH}; color:white; }}
  .badge-akan    {{ background:{KELABU};    color:white; }}

  /* ── Section title ── */
  .section-title {{
      font-size: 1rem;
      font-weight: 700;
      color: {BIRU_GELAP};
      border-left: 4px solid {EMAS};
      padding-left: 10px;
      margin: 24px 0 12px 0;
  }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, {BIRU_GELAP} 0%, {BIRU_SEDANG} 100%);
  }}
  [data-testid="stSidebar"] * {{ color: white !important; }}
  [data-testid="stSidebar"] .stSelectbox label {{ color: {EMAS_CERAH} !important; font-weight: 700; }}
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {{ color: {EMAS_CERAH} !important; }}
  [data-testid="stSidebar"] .stMarkdown p {{ color: #B8D0F0 !important; }}

  /* ── Table ── */
  .custom-table {{ width:100%; border-collapse:collapse; font-size:0.84rem; }}
  .custom-table th {{
      background:{BIRU_GELAP}; color:{EMAS_CERAH};
      padding:10px 12px; text-align:left; font-weight:700;
  }}
  .custom-table td {{ padding:9px 12px; border-bottom:1px solid #E5EAF2; }}
  .custom-table tr:nth-child(even) {{ background:#F7FAFF; }}
  .custom-table tr:hover {{ background:{BIRU_LEMBUT}; }}

  .badge-s {{ background:{HIJAU};     color:white; border-radius:4px; padding:2px 8px; font-size:0.75rem; font-weight:700; }}
  .badge-a {{ background:{BIRU_CERAH};color:white; border-radius:4px; padding:2px 8px; font-size:0.75rem; font-weight:700; }}
  .badge-b {{ background:{KELABU};    color:white; border-radius:4px; padding:2px 8px; font-size:0.75rem; font-weight:700; }}

  /* ── Footer ── */
  .footer {{
      text-align:center; color:{KELABU}; font-size:0.76rem;
      border-top:1px solid #DDE3EE; padding-top:14px; margin-top:28px;
  }}
  div[data-testid="stMetricValue"] {{ font-size: 1.8rem !important; }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA JADUAL GILIRAN
# ─────────────────────────────────────────────
JADUAL_GILIRAN = {
    2027: "JRKV",
    2028: "JKM",
    2029: "JPH",
    2030: "JPA",
    2031: "JP",
    2032: "JMSK",
    2033: "JTMK",
}
NAMA_JABATAN = {
    "JRKV" : "Jabatan Rekabentuk & Kejuruteraan Vokasional",
    "JKM"  : "Jabatan Kejuruteraan Mekanikal",
    "JPH"  : "Jabatan Perhotelan",
    "JPA"  : "Jabatan Perakaunan",
    "JP"   : "Jabatan Perdagangan",
    "JMSK" : "Jabatan Matematik, Sains & Komputer",
    "JTMK" : "Jabatan Teknologi Maklumat & Komunikasi",
}
TAHUN_SENARAI = list(JADUAL_GILIRAN.keys())

# ─────────────────────────────────────────────
#  MUATKAN DATA CSV
# ─────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "data_kikhb.csv")

@st.cache_data(ttl=60)
def muatkan_data():
    df = pd.read_csv(DATA_PATH)
    df["tahun"] = df["tahun"].astype(int)
    df["peratusan"] = pd.to_numeric(df["peratusan"], errors="coerce").fillna(0)
    return df

df_semua = muatkan_data()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏛️ KIKHB PMS")
    st.markdown("**Politeknik Muadzam Shah**")
    st.markdown("---")
    st.markdown("### 📅 Pilih Tahun")
    tahun_dipilih = st.selectbox(
        "Tahun Giliran:",
        options=TAHUN_SENARAI,
        index=TAHUN_SENARAI.index(2030),  # default: tahun aktif semasa
        format_func=lambda y: f"{y} — {JADUAL_GILIRAN[y]}",
    )
    st.markdown("---")
    st.markdown("### 📋 Jadual Giliran")
    for t, j in JADUAL_GILIRAN.items():
        marker = "▶" if t == tahun_dipilih else "·"
        st.markdown(f"`{marker}` **{t}** — {j}")
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.75rem;'>📂 Data dimuatkan daripada<br><code>data_kikhb.csv</code></p>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  HEADER UTAMA
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="main-header">
      <h1>🏛️ Dashboard KPI — KIK Horizon Baharu (KIKHB)</h1>
      <p>Politeknik Muadzam Shah (PMS) &nbsp;|&nbsp; Pemantauan Kemajuan Giliran Jabatan 2027–2033</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  BANNER AMARAN TERKINI
# ─────────────────────────────────────────────
jabatan_aktif    = JADUAL_GILIRAN[tahun_dipilih]
nama_aktif       = NAMA_JABATAN.get(jabatan_aktif, jabatan_aktif)
tahun_akan_datang = tahun_dipilih + 1
jabatan_akan_datang = JADUAL_GILIRAN.get(tahun_akan_datang)
nama_akan_datang = NAMA_JABATAN.get(jabatan_akan_datang, jabatan_akan_datang) if jabatan_akan_datang else None

st.markdown(
    f"""
    <div class="banner-aktif">
      🔵 &nbsp;<strong>JABATAN BERTUGAS {tahun_dipilih}:</strong> &nbsp;
      <span style="color:{EMAS_CERAH}; font-size:1.1rem; font-weight:800;">{jabatan_aktif}</span>
      &nbsp;— {nama_aktif}
    </div>
    """,
    unsafe_allow_html=True,
)

if jabatan_akan_datang:
    st.markdown(
        f"""
        <div class="banner-akan-datang">
          ⚠️ &nbsp;<strong>AMARAN GILIRAN SETERUSNYA ({tahun_akan_datang}):</strong> &nbsp;
          Jabatan <strong>{jabatan_akan_datang}</strong> ({nama_akan_datang}) perlu mula
          membuat persediaan awal untuk giliran mereka.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """<div class="banner-akan-datang">ℹ️ Ini adalah tahun giliran terakhir dalam kitaran 2027–2033.</div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  GARIS MASA VISUAL (TIMELINE CARDS)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📆 Garis Masa Giliran KIKHB 2027–2033</div>', unsafe_allow_html=True)

def statuskan_tahun(t):
    if t < tahun_dipilih:
        return "Selesai"
    elif t == tahun_dipilih:
        return "Aktif"
    else:
        return "Akan Datang"

tl_html = '<div class="timeline-wrap">'
for t, j in JADUAL_GILIRAN.items():
    s = statuskan_tahun(t)
    if s == "Selesai":
        kelas_card  = "tl-card tl-selesai"
        kelas_badge = "tl-badge badge-selesai"
        icon        = "✅"
    elif s == "Aktif":
        kelas_card  = "tl-card tl-aktif"
        kelas_badge = "tl-badge badge-aktif"
        icon        = "🔵"
    else:
        kelas_card  = "tl-card tl-akan"
        kelas_badge = "tl-badge badge-akan"
        icon        = "🔲"

    tl_html += f"""
    <div class="{kelas_card}">
      <div style="font-size:1.3rem;">{icon}</div>
      <div style="font-size:1.05rem; font-weight:800; margin:4px 0;">{t}</div>
      <div style="font-size:0.9rem; font-weight:700;">{j}</div>
      <div class="{kelas_badge}">{s}</div>
    </div>"""
tl_html += "</div>"
st.markdown(tl_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DATA UNTUK TAHUN DIPILIH
# ─────────────────────────────────────────────
df_tahun = df_semua[df_semua["tahun"] == tahun_dipilih].copy()

# ─────────────────────────────────────────────
#  KPI CARDS (4 KARTAD)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Petunjuk Prestasi Utama (KPI)</div>', unsafe_allow_html=True)

# Kira KPI
jumlah_milestone  = len(df_tahun)
selesai_count     = len(df_tahun[df_tahun["status"] == "Selesai"])
aktif_count       = len(df_tahun[df_tahun["status"] == "Aktif"])
pct_kemajuan      = round((df_tahun["peratusan"].mean()), 1) if jumlah_milestone > 0 else 0

fasa_list = df_tahun["fasa"].unique()
fasa_selesai = 0
for f in fasa_list:
    df_f = df_tahun[df_tahun["fasa"] == f]
    if all(df_f["status"] == "Selesai"):
        fasa_selesai += 1

# Status sasaran konvensyen
konvensyen_df  = df_tahun[df_tahun["fasa"] == "Fasa 4: Konvensyen"]
pct_konvensyen = round(konvensyen_df["peratusan"].mean(), 0) if len(konvensyen_df) > 0 else 0
if pct_konvensyen == 100:
    status_konvensyen = "✅ Tercapai"
    warna_konvensyen  = HIJAU
elif pct_konvensyen > 0:
    status_konvensyen = "⏳ Dalam Proses"
    warna_konvensyen  = BIRU_CERAH
else:
    status_konvensyen = "⏸ Belum Mula"
    warna_konvensyen  = KELABU

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""<div class="kpi-card">
          <div class="kpi-label">🏢 Jabatan Bertugas</div>
          <div class="kpi-value" style="font-size:1.6rem; color:{BIRU_GELAP};">{jabatan_aktif}</div>
          <div class="kpi-sub">{tahun_dipilih}</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c2:
    warna_pct = HIJAU if pct_kemajuan >= 80 else (EMAS if pct_kemajuan >= 40 else MERAH)
    st.markdown(
        f"""<div class="kpi-card kpi-card-emas">
          <div class="kpi-label">📈 % Kemajuan Keseluruhan</div>
          <div class="kpi-value" style="color:{warna_pct};">{pct_kemajuan}%</div>
          <div class="kpi-sub">{selesai_count}/{jumlah_milestone} tugasan selesai</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""<div class="kpi-card kpi-card-hijau">
          <div class="kpi-label">✅ Fasa Selesai</div>
          <div class="kpi-value kpi-value-hijau">{fasa_selesai}</div>
          <div class="kpi-sub">daripada {len(fasa_list)} fasa</div>
        </div>""",
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""<div class="kpi-card">
          <div class="kpi-label">🏆 Status Sasaran Konvensyen</div>
          <div class="kpi-value" style="font-size:1.1rem; color:{warna_konvensyen};">{status_konvensyen}</div>
          <div class="kpi-sub">{int(pct_konvensyen)}% kemajuan Fasa 4</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CARTA BAR KEMAJUAN MENGIKUT FASA
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📉 Kemajuan Mengikut Fasa KIKHB</div>', unsafe_allow_html=True)

WARNA_FASA = [BIRU_GELAP, BIRU_SEDANG, BIRU_CERAH, EMAS, "#7B4FA0"]

fasa_kemajuan = (
    df_tahun.groupby("fasa")["peratusan"]
    .mean()
    .reset_index()
    .rename(columns={"peratusan": "kemajuan_avg"})
)
fasa_kemajuan["kemajuan_avg"] = fasa_kemajuan["kemajuan_avg"].round(1)

URUTAN_FASA = [
    "Fasa 1: Persediaan",
    "Fasa 2: Pelaksanaan",
    "Fasa 3: Pemantauan",
    "Fasa 4: Konvensyen",
    "Fasa 5: Penutupan",
]
fasa_kemajuan["fasa"] = pd.Categorical(fasa_kemajuan["fasa"], categories=URUTAN_FASA, ordered=True)
fasa_kemajuan = fasa_kemajuan.sort_values("fasa")

fig_bar = go.Figure()
for i, row in fasa_kemajuan.iterrows():
    idx = URUTAN_FASA.index(row["fasa"]) if row["fasa"] in URUTAN_FASA else 0
    warna = WARNA_FASA[idx % len(WARNA_FASA)]
    fig_bar.add_trace(
        go.Bar(
            x=[row["fasa"]],
            y=[row["kemajuan_avg"]],
            name=row["fasa"],
            marker_color=warna,
            text=f"{row['kemajuan_avg']}%",
            textposition="outside",
            showlegend=False,
        )
    )

fig_bar.add_hline(
    y=100, line_dash="dot", line_color=HIJAU,
    annotation_text="Sasaran 100%", annotation_position="top right",
    annotation_font_color=HIJAU,
)

fig_bar.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter, sans-serif", size=12, color=BIRU_GELAP),
    yaxis=dict(title="% Kemajuan", range=[0, 115], showgrid=True, gridcolor="#EEF2F9"),
    xaxis=dict(title="Fasa KIKHB"),
    height=380,
    margin=dict(t=30, b=20, l=40, r=20),
    bargap=0.35,
)

st.plotly_chart(fig_bar, use_container_width=True)

# ─────────────────────────────────────────────
#  JADUAL SENARAI SEMAK TUGASAN (MILESTONES)
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Senarai Semak Tugasan (Milestones)</div>', unsafe_allow_html=True)

col_filter, col_spacer = st.columns([2, 4])
with col_filter:
    fasa_pilihan = st.selectbox(
        "Tapis mengikut Fasa:",
        options=["Semua Fasa"] + URUTAN_FASA,
        key="fasa_filter",
    )

df_papar = df_tahun.copy()
if fasa_pilihan != "Semua Fasa":
    df_papar = df_papar[df_papar["fasa"] == fasa_pilihan]

def render_badge(status):
    if status == "Selesai":
        return f'<span class="badge-s">✅ Selesai</span>'
    elif status == "Aktif":
        return f'<span class="badge-a">🔵 Aktif</span>'
    else:
        return f'<span class="badge-b">⏸ Belum Mula</span>'

rows_html = ""
for _, r in df_papar.iterrows():
    bar_w   = int(r["peratusan"])
    bar_col = HIJAU if bar_w == 100 else (BIRU_CERAH if bar_w > 0 else "#BDBDBD")
    progress_bar = f"""
      <div style="background:#E8EAED; border-radius:4px; height:8px; width:120px; display:inline-block; vertical-align:middle;">
        <div style="background:{bar_col}; width:{bar_w}%; height:100%; border-radius:4px;"></div>
      </div>
      <span style="font-size:0.75rem; color:{KELABU}; margin-left:5px;">{bar_w}%</span>
    """
    rows_html += f"""
    <tr>
      <td><strong>{r['fasa']}</strong></td>
      <td>{r['milestone']}</td>
      <td>{render_badge(r['status'])}</td>
      <td>{progress_bar}</td>
      <td>{r['tarikh_mula']}</td>
      <td>{r['tarikh_tamat']}</td>
    </tr>"""

table_html = f"""
<table class="custom-table">
  <thead>
    <tr>
      <th>Fasa</th><th>Milestone / Tugasan</th><th>Status</th>
      <th>Kemajuan</th><th>Tarikh Mula</th><th>Tarikh Tamat</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  RINGKASAN STATISTIK
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📌 Ringkasan Status Semua Tahun</div>', unsafe_allow_html=True)

rows_summary = ""
for t, j in JADUAL_GILIRAN.items():
    df_t     = df_semua[df_semua["tahun"] == t]
    pct_avg  = round(df_t["peratusan"].mean(), 1) if len(df_t) > 0 else 0
    sel      = len(df_t[df_t["status"] == "Selesai"])
    total    = len(df_t)
    s_tahun  = statuskan_tahun(t)
    badge_t  = render_badge("Selesai") if s_tahun == "Selesai" else (render_badge("Aktif") if s_tahun == "Aktif" else render_badge("Belum Mula"))
    bar_col  = HIJAU if pct_avg == 100 else (BIRU_CERAH if pct_avg > 0 else "#BDBDBD")
    bar_html = f"""
      <div style="background:#E8EAED;border-radius:4px;height:10px;width:150px;display:inline-block;vertical-align:middle;">
        <div style="background:{bar_col};width:{pct_avg}%;height:100%;border-radius:4px;"></div>
      </div>
      <span style="font-size:0.78rem;color:{KELABU};margin-left:6px;">{pct_avg}%</span>
    """
    rows_summary += f"""
    <tr>
      <td><strong>{t}</strong></td>
      <td><strong>{j}</strong></td>
      <td style="font-size:0.8rem; color:{KELABU};">{NAMA_JABATAN.get(j,'')}</td>
      <td>{badge_t}</td>
      <td>{bar_html}</td>
      <td>{sel}/{total}</td>
    </tr>"""

summary_html = f"""
<table class="custom-table">
  <thead>
    <tr><th>Tahun</th><th>Jabatan</th><th>Nama Penuh</th><th>Status</th><th>Kemajuan</th><th>Tugasan</th></tr>
  </thead>
  <tbody>{rows_summary}</tbody>
</table>
"""
st.markdown(summary_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  NOTA CARA KEMASKINI DATA
# ─────────────────────────────────────────────
with st.expander("ℹ️ Cara Kemaskini Data Dashboard"):
    st.markdown(
        f"""
        **Dashboard ini membaca data secara langsung daripada fail `data_kikhb.csv`.**

        Untuk mengemaskini status atau kemajuan sesuatu tugasan:
        1. Buka fail `data_kikhb.csv` menggunakan Microsoft Excel atau editor teks.
        2. Cari baris yang berkaitan (berdasarkan `tahun`, `jabatan`, dan `milestone`).
        3. Kemaskini lajur **`status`** kepada salah satu nilai: `Selesai`, `Aktif`, atau `Belum Mula`.
        4. Kemaskini lajur **`peratusan`** kepada nilai 0–100.
        5. Simpan fail dan **reload** halaman dashboard ini (tekan `R` atau klik butang reload).

        | Lajur | Nilai Dibenarkan |
        |---|---|
        | `status` | `Selesai` / `Aktif` / `Belum Mula` |
        | `peratusan` | `0` hingga `100` |
        | `tahun` | `2027` hingga `2033` |
        | `jabatan` | `JRKV`, `JKM`, `JPH`, `JPA`, `JP`, `JMSK`, `JTMK` |
        """,
        unsafe_allow_html=False,
    )

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown(
    f"""
    <div class="footer">
      🏛️ Dashboard KPI KIKHB &nbsp;|&nbsp; Politeknik Muadzam Shah (PMS) &nbsp;|&nbsp;
      Data dimuatkan: <code>{DATA_PATH}</code><br>
      <span style="font-size:0.7rem;">Versi 1.0 &nbsp;·&nbsp; Dibangunkan menggunakan Streamlit &amp; Plotly</span>
    </div>
    """,
    unsafe_allow_html=True,
)
