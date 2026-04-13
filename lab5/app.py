import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#1. Налаштування сторінки
st.set_page_config(layout="wide", page_title="VHI Analysis")
st.title("Наука про дані: Лабораторна робота №5")

#2. Завантаження даних
@st.cache_data
def load_vhi_data():
    vhi_df = pd.read_csv('vhi_data.csv')
    vhi_df['Year'] = vhi_df['Year'].astype(int)
    vhi_df['Week'] = vhi_df['Week'].astype(int)
    return vhi_df

try:
    main_dataframe = load_vhi_data()
except Exception:
    st.error("Файл 'vhi_data.csv' не знайдено!")
    st.stop()

#3. Логіка скидання
def reset_all_filters():
    st.session_state.index_key = "VHI"
    st.session_state.region_key = main_dataframe['Region'].unique()[0]
    st.session_state.week_range_key = (1, 52)
    st.session_state.year_range_key = (int(main_dataframe['Year'].min()), int(main_dataframe['Year'].max()))
    st.session_state.asc_key = False
    st.session_state.desc_key = False

if 'index_key' not in st.session_state:
    reset_all_filters()

#4. Бічна панель
with st.sidebar:
    st.header("Параметри")
    
    selected_index = st.selectbox("Оберіть часовий ряд:", ["VCI", "TCI", "VHI"], key="index_key")
    selected_region = st.selectbox("Оберіть область:", main_dataframe['Region'].unique(), key="region_key")
    selected_weeks = st.slider("Тижні:", 1, 52, key="week_range_key")
    selected_years = st.slider("Роки:", int(main_dataframe['Year'].min()), int(main_dataframe['Year'].max()), key="year_range_key")
    
    st.subheader("Сортування")
    sort_ascending = st.checkbox("За зростанням", key="asc_key")
    sort_descending = st.checkbox("За спаданням", key="desc_key")
    
    if sort_ascending and sort_descending:
        st.warning("Вибрано обидва типи сортування. Пріоритет: За зростанням.")

    st.button("Reset", on_click=reset_all_filters)

# 5. Фільтрація та сортування
filtered_data = main_dataframe[
    (main_dataframe['Region'] == selected_region) & 
    (main_dataframe['Year'].between(selected_years[0], selected_years[1])) & 
    (main_dataframe['Week'].between(selected_weeks[0], selected_weeks[1]))
].copy()

if sort_ascending:
    filtered_data = filtered_data.sort_values(by=selected_index, ascending=True)
elif sort_descending:
    filtered_data = filtered_data.sort_values(by=selected_index, ascending=False)

# 6. Вкладки
tab_table, tab_region_plot, tab_comparison = st.tabs(["Таблиця", "Графік області", "Порівняння"])

with tab_table:
    st.subheader(f"Дані для {selected_region}")
    
    pearson = filtered_data[selected_index].corr(filtered_data['Year'], method='pearson')
    spearman = filtered_data[selected_index].corr(filtered_data['Year'], method='spearman')
    st.write(f"**Кореляція {selected_index} з роком:** Пірсон: {pearson:.3f}, Спірмен: {spearman:.3f}")
    
    if st.checkbox("Показати One Hot Encoding області"):
        ohe_demo = pd.get_dummies(filtered_data, columns=['Region'])
        st.dataframe(ohe_demo.head())
    else:
        st.dataframe(filtered_data, width='stretch') 

with tab_region_plot:
    st.subheader(f"Динаміка {selected_index}")
    plot_df = filtered_data.sort_values(by=['Year', 'Week'])
    plot_df['Time'] = plot_df['Year'].astype(str) + "-W" + plot_df['Week'].astype(str).str.zfill(2)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(plot_df['Time'], plot_df[selected_index])
    
    step = max(len(plot_df) // 10, 1)
    ax.set_xticks(plot_df['Time'][::step])
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab_comparison:
    st.subheader(f"Порівняння {selected_index} обраної області з іншими")
    
    compare_df = main_dataframe[
        (main_dataframe['Year'].between(selected_years[0], selected_years[1])) & 
        (main_dataframe['Week'].between(selected_weeks[0], selected_weeks[1]))
    ].copy()
    
    compare_df = compare_df.sort_values(by=['Year', 'Week'])
    compare_df['Time'] = compare_df['Year'].astype(str) + "-W" + compare_df['Week'].astype(str).str.zfill(2)
    
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    for r in compare_df['Region'].unique():
        region_subset = compare_df[compare_df['Region'] == r]
        
        if r == selected_region:
            ax2.plot(region_subset['Time'], region_subset[selected_index], label=r, color='red', linewidth=2.5, zorder=5)
        else:
            ax2.plot(region_subset['Time'], region_subset[selected_index], color='gray', alpha=0.15, linewidth=0.7)
    
    time_ticks = compare_df['Time'].unique()
    tick_step = max(len(time_ticks) // 10, 1)
    ax2.set_xticks(time_ticks[::tick_step])
    plt.xticks(rotation=45)
    
    ax2.set_ylabel(selected_index)
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.2)
    
    st.pyplot(fig2)
