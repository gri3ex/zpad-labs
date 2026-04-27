import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Налаштування сторінки (п. 21)
st.set_page_config(layout="wide", page_title="VHI Analysis")
st.title("Наука про дані: Лабораторна робота №5")

# 2. Завантаження даних (п. 10)
@st.cache_data
def load_data():
    df = pd.read_csv('vhi_data.csv')
    df['Year'] = df['Year'].astype(int)
    df['Week'] = df['Week'].astype(int)
    return df

try:
    df = load_data()
except Exception:
    st.error("Файл 'vhi_data.csv' не знайдено!")
    st.stop()

# 3. Логіка скидання (п. 14)
def reset_all_filters():
    st.session_state.idx = "VHI"
    st.session_state.reg = df['Region'].unique()[0]
    st.session_state.weeks = (1, 52)
    st.session_state.years = (int(df['Year'].min()), int(df['Year'].max()))
    st.session_state.s_asc = False
    st.session_state.s_desc = False

if 'idx' not in st.session_state:
    reset_all_filters()

# 4. Бічна панель (п. 21)
with st.sidebar:
    st.header("Параметри")
    
    # Віджети з ключами (п. 10-13)
    idx_choice = st.selectbox("Оберіть часовий ряд:", ["VCI", "TCI", "VHI"], key="idx")
    reg_choice = st.selectbox("Оберіть область:", df['Region'].unique(), key="reg")
    w_range = st.slider("Тижні:", 1, 52, key="weeks")
    y_range = st.slider("Роки:", int(df['Year'].min()), int(df['Year'].max()), key="years")
    
    st.subheader("Сортування")
    # Чекбокси (п. 19)
    sort_asc = st.checkbox("За зростанням", key="s_asc")
    sort_desc = st.checkbox("За спаданням", key="s_desc")
    
    if sort_asc and sort_desc: # п. 20 [cite: 20]
        st.warning("Вибрано обидва типи сортування. Пріоритет: За зростанням.")

    # Кнопка Reset з callback (п. 14)
    st.button("Reset" , on_click=reset_all_filters)

# 5. Фільтрація та сортування
f_df = df[
    (df['Region'] == reg_choice) & 
    (df['Year'].between(y_range[0], y_range[1])) & 
    (df['Week'].between(w_range[0], w_range[1]))
].copy()

if sort_asc:
    f_df = f_df.sort_values(by=idx_choice, ascending=True)
elif sort_desc:
    f_df = f_df.sort_values(by=idx_choice, ascending=False)

# 6. Вкладки (п. 15, 21)
t1, t2, t3 = st.tabs(["Таблиця", "Графік області", "Порівняння"])

with t1:
    st.subheader(f"Дані для {reg_choice}")
    st.dataframe(f_df, width='stretch') 

with t2:
    st.subheader(f"Динаміка {idx_choice}") # п. 16 
    p_df = f_df.sort_values(by=['Year', 'Week'])
    p_df['Time'] = p_df['Year'].astype(str) + "-W" + p_df['Week'].astype(str).str.zfill(2)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(p_df['Time'], p_df[idx_choice])
    
    step = max(len(p_df) // 10, 1)
    ax.set_xticks(p_df['Time'][::step])
    plt.xticks(rotation=45)
    st.pyplot(fig)

with t3:
    st.subheader(f"Порівняння {idx_choice} обраної області з іншими")
    
    # 1. Готую дані для порівняння та сортую їх хронологічно
    compare_df = df[
        (df['Year'].between(y_range[0], y_range[1])) & 
        (df['Week'].between(w_range[0], w_range[1]))
    ].copy()
    
    # Створюю вісь часу для плавних ліній
    compare_df = compare_df.sort_values(by=['Year', 'Week'])
    compare_df['Time'] = compare_df['Year'].astype(str) + "-W" + compare_df['Week'].astype(str).str.zfill(2)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    # 2. Малюю кожну область окремо (п. 17)
    for r in compare_df['Region'].unique():
        region_data = compare_df[compare_df['Region'] == r]
        
        # Виділяю обрану область червоним, інші роблю сірими та прозорими
        if r == reg_choice:
            ax2.plot(region_data['Time'], region_data[idx_choice], label=r, color='red', linewidth=2.5, zorder=5)
        else:
            ax2.plot(region_data['Time'], region_data[idx_choice], color='gray', alpha=0.15, linewidth=0.7)
    
    # 3. Налаштовую вісь X, щоб підписи не зливалися (п. 18)
    time_ticks = compare_df['Time'].unique()
    step = max(len(time_ticks) // 10, 1)
    ax2.set_xticks(time_ticks[::step])
    plt.xticks(rotation=45)
    
    ax2.set_ylabel(idx_choice)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.2)
    
    st.pyplot(fig2)