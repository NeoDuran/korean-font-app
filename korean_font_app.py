import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly import offline
import platform

# 페이지 설정
st.set_page_config(
    page_title="한글 폰트 테스트",
    page_icon="🇰🇷",
    layout="wide"
)

# 한글 폰트 설정 함수
@st.cache_resource
def setup_korean_font():
    """
    운영체제별로 한글 폰트를 설정하는 함수
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows에서 사용 가능한 한글 폰트
        font_candidates = ['Malgun Gothic', 'Microsoft YaHei', 'SimHei']
    elif system == "Darwin":  # macOS
        # macOS에서 사용 가능한 한글 폰트
        font_candidates = ['AppleGothic', 'Apple SD Gothic Neo', 'Noto Sans CJK KR']
    else:  # Linux
        # Linux에서 사용 가능한 한글 폰트
        font_candidates = ['Noto Sans CJK KR', 'DejaVu Sans', 'Liberation Sans']
    
    # 사용 가능한 폰트 찾기
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    selected_font = None
    for font in font_candidates:
        if font in available_fonts:
            selected_font = font
            break
    
    if selected_font:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
        st.success(f"✅ 한글 폰트 설정 완료: {selected_font}")
        return selected_font
    else:
        st.warning("⚠️ 적절한 한글 폰트를 찾을 수 없습니다. 기본 폰트를 사용합니다.")
        # 폰트 파일을 직접 로드하는 방법 (선택사항)
        try:
            # 만약 프로젝트 폴더에 한글 폰트 파일이 있다면
            font_path = "NotoSansKR-Regular.ttf"  # 폰트 파일 경로
            font_prop = fm.FontProperties(fname=font_path)
            plt.rcParams['font.family'] = font_prop.get_name()
            plt.rcParams['axes.unicode_minus'] = False
            st.success(f"✅ 폰트 파일에서 한글 폰트 로드 완료")
            return font_prop.get_name()
        except:
            st.error("❌ 한글 폰트 설정에 실패했습니다.")
            return None

def main():
    # 한글 폰트 설정
    font_name = setup_korean_font()
    
    st.title("🇰🇷 Streamlit 한글 폰트 테스트")
    st.markdown("---")
    
    # 사이드바
    st.sidebar.header("📊 차트 옵션")
    chart_type = st.sidebar.selectbox(
        "차트 유형 선택",
        ["막대 차트", "선 그래프", "파이 차트", "히트맵", "산점도"]
    )
    
    # 샘플 데이터 생성
    data = {
        '지역': ['서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종'],
        '인구수': [9720846, 3404423, 2401110, 2947217, 1441970, 1454679, 1124459, 365309],
        '면적': [605.21, 770.18, 883.56, 1040.82, 501.31, 539.98, 1061.4, 465.23],
        '인구밀도': [16154, 4419, 2716, 2831, 2876, 2694, 1059, 785]
    }
    df = pd.DataFrame(data)
    
    # 메인 컨텐츠
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📈 차트 영역")
        
        if chart_type == "막대 차트":
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(df['지역'], df['인구수'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'])
            ax.set_title('지역별 인구수', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('지역', fontsize=12)
            ax.set_ylabel('인구수 (명)', fontsize=12)
            
            # 막대 위에 값 표시
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 50000,
                       f'{int(height):,}', ha='center', va='bottom', fontsize=10)
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
        elif chart_type == "선 그래프":
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['지역'], df['인구밀도'], marker='o', linewidth=2, markersize=8, color='#FF6B6B')
            ax.set_title('지역별 인구밀도', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('지역', fontsize=12)
            ax.set_ylabel('인구밀도 (명/㎢)', fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
        elif chart_type == "파이 차트":
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
            wedges, texts, autotexts = ax.pie(df['인구수'], labels=df['지역'], autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
            ax.set_title('지역별 인구 비율', fontsize=16, fontweight='bold', pad=20)
            
            # 텍스트 크기 조정
            for text in texts:
                text.set_fontsize(11)
            for autotext in autotexts:
                autotext.set_fontsize(10)
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            st.pyplot(fig)
            
        elif chart_type == "히트맵":
            # 상관관계 히트맵을 위한 데이터 준비
            numeric_df = df[['인구수', '면적', '인구밀도']]
            correlation_matrix = numeric_df.corr()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5, ax=ax)
            ax.set_title('인구수, 면적, 인구밀도 상관관계', fontsize=16, fontweight='bold', pad=20)
            st.pyplot(fig)
            
        elif chart_type == "산점도":
            fig, ax = plt.subplots(figsize=(10, 6))
            scatter = ax.scatter(df['면적'], df['인구수'], s=df['인구밀도']/30, 
                               alpha=0.7, c=range(len(df)), cmap='viridis')
            
            # 각 점에 지역명 라벨 추가
            for i, txt in enumerate(df['지역']):
                ax.annotate(txt, (df['면적'].iloc[i], df['인구수'].iloc[i]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=10)
            
            ax.set_title('면적 vs 인구수 (버블 크기: 인구밀도)', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('면적 (㎢)', fontsize=12)
            ax.set_ylabel('인구수 (명)', fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        st.header("📊 데이터 테이블")
        st.dataframe(df, use_container_width=True)
        
        st.header("📝 한글 텍스트 테스트")
        st.write("**한글 표시 테스트:**")
        st.write("• 안녕하세요! 👋")
        st.write("• 한글이 잘 표시되나요?")
        st.write("• 특수문자: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ")
        
        # 메트릭 표시
        st.header("📈 주요 지표")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("총 인구수", f"{df['인구수'].sum():,}명")
            st.metric("평균 면적", f"{df['면적'].mean():.1f}㎢")
        with col_b:
            st.metric("최고 인구밀도", f"{df['인구밀도'].max():,}명/㎢")
            st.metric("최저 인구밀도", f"{df['인구밀도'].min():,}명/㎢")
    
    # Plotly 차트 (추가 테스트)
    st.markdown("---")
    st.header("🎨 Plotly 한글 차트 테스트")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Plotly 막대 차트
        fig_plotly = px.bar(df, x='지역', y='인구수', 
                           title='지역별 인구수 (Plotly)',
                           color='인구수',
                           color_continuous_scale='viridis')
        fig_plotly.update_layout(
            font=dict(family="Malgun Gothic, AppleGothic, Noto Sans CJK KR", size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_plotly, use_container_width=True)
    
    with col4:
        # Plotly 도넛 차트
        fig_donut = go.Figure(data=[go.Pie(labels=df['지역'], values=df['인구수'], hole=.3)])
        fig_donut.update_layout(
            title="지역별 인구 비율 (도넛 차트)",
            font=dict(family="Malgun Gothic, AppleGothic, Noto Sans CJK KR", size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    
    # 폰트 정보 표시
    st.markdown("---")
    with st.expander("🔧 폰트 설정 정보"):
        st.write(f"**현재 시스템:** {platform.system()}")
        st.write(f"**설정된 폰트:** {font_name}")
        st.write(f"**Matplotlib 폰트 패밀리:** {plt.rcParams['font.family']}")
        
        # 사용 가능한 한글 폰트 목록
        available_fonts = [f.name for f in fm.fontManager.ttflist if 'Gothic' in f.name or 'Noto' in f.name or 'Malgun' in f.name]
        if available_fonts:
            st.write("**사용 가능한 한글 폰트:**")
            for font in available_fonts[:10]:  # 상위 10개만 표시
                st.write(f"- {font}")

if __name__ == "__main__":
    main()