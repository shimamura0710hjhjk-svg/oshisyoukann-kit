import streamlit as st
import json
import os



# --- フォルダ準備 ---
CHAR_DIR = "characters"
USER_DIR = "users"
os.makedirs(CHAR_DIR, exist_ok=True)
os.makedirs(USER_DIR, exist_ok=True)
USER_FILE = os.path.join(USER_DIR, "me.json")

st.set_page_config(page_title="推し召喚管理", layout="wide")
st.markdown("""
    <style>
    /* 全体の背景をさらに暗く、文字を読みやすく */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }

    /* ボタンを大きく、押しやすく（スマホの親指用） */
    div.stButton > button {
        width: 100%;
        height: 3em;
        border-radius: 10px;
        background-color: #262730;
        border: 1px solid #4b4b4b;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* 感情別ボタンの色分け（視覚的にわかりやすく） */
    div.stButton > button:active {
        background-color: #ff4b4b; /* 押し心地を出す */
    }

    /* テキストエリアの見た目（官能小説風のフォント） */
    textarea {
        font-family: 'Noto Serif JP', serif !important;
        background-color: #161b22 !important;
    }

    /* 音声プレイヤーをコンパクトに */
    audio {
        width: 100%;
        height: 40px;
    }
    
    /* 画像を丸くして「アイコン」っぽくする */
    img {
        border-radius: 50%;
        border: 2px solid #af966e; /* 推し君Aに合わせたゴールド枠 */
    }
    </style>
    """, unsafe_allow_html=True)
st.title("💎 推し召喚・全設定管理システム")

# --- 1. 夢主（あなた）の設定セクション ---
with st.sidebar:
    st.header("👤 夢主（自分）の情報")
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            user_data = json.load(f)
    else:
        user_data = {"name": "", "mbti": "INFP", "traits": "", "weakness": ""}

    with st.form("user_form"):
        user_data["name"] = st.text_input("あなたの名前", user_data["name"])
        user_data["mbti"] = st.selectbox("自分のMBTI", ["INTJ", "INFP", "INFJ", "ENFP", "ISTP", "ISFJ", "ENTP"], index=0)
        user_data["traits"] = st.text_area("特徴（身長差や性格）", user_data["traits"], help="例：155cm、おっとりしている、断れない性格")
        user_data["weakness"] = st.text_area("弱点", user_data["weakness"], help="例：耳元での囁き、強引な態度")
        if st.form_submit_button("自分設定を保存"):
            with open(USER_FILE, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            st.success("自分の情報を更新したにゃ！")

# --- 2. キャラクター設定セクション ---
char_files = [f for f in os.listdir(CHAR_DIR) if f.endswith(".json")]
mode = st.radio("作業を選択", ["既存キャラの編集", "新しいキャラを追加"], horizontal=True)

# デフォルト値の設定
default_char = {
    "name": "", "age": 30, "sexuality": "男性", "mbti": "INTJ",
    "first_person": "俺", "second_person": "お前",
    "job": "", "hobby": "", "likes": "", "dislikes": "",
    "traits": "", "personality": "",
    "voice_sample": "", "prompt_text": "", "voice_dir": "",
    "emotions": {"default": "refer_normal.wav", "whisper": "refer_sexy.wav", "stress": "refer_angry.wav"},
    "response_templates": {"default": "", "whisper": "", "stress": ""}
}

if mode == "既存キャラの編集" and char_files:
    selected_file = st.selectbox("編集するキャラを選択", char_files)
    with open(os.path.join(CHAR_DIR, selected_file), "r", encoding="utf-8") as f:
        current_char = json.load(f)
else:
    current_char = default_char
    selected_file = st.text_input("新規保存ファイル名 (例: oshi_b.json)")

# 入力フォーム
with st.form("main_form"):
    col1, col2, col3 = st.columns(3)
    current_char["name"] = col1.text_input("名前", current_char.get("name", ""))
    current_char["age"] = col2.number_input("年齢", value=current_char.get("age", 20))
    current_char["mbti"] = col3.text_input("MBTI", current_char.get("mbti", ""))

    col4, col5, col6 = st.columns(3)
    current_char["sexuality"] = col4.text_input("性別/性自認", current_char.get("sexuality", "男性"))
    current_char["first_person"] = col5.text_input("一人称", current_char.get("first_person", "俺"))
    current_char["second_person"] = col6.text_input("二人称", current_char.get("second_person", "お前"))

    st.subheader("基本属性")
    col_a, col_b = st.columns(2)
    current_char["job"] = col_a.text_input("職業", current_char.get("job", ""))
    current_char["hobby"] = col_b.text_input("趣味", current_char.get("hobby", ""))
    current_char["likes"] = col_a.text_input("好きなもの", current_char.get("likes", ""))
    current_char["dislikes"] = col_b.text_input("嫌いなもの", current_char.get("dislikes", ""))

    current_char["traits"] = st.text_input("特徴（短いタグ風に）", current_char.get("traits", ""), help="たばこを吸う、独占欲が強い、など")
    current_char["personality"] = st.text_area("性格詳細（プロンプトに強く影響します）", current_char.get("personality", ""))

    st.subheader("音声・ボイス管理")
    current_char["voice_dir"] = st.text_input("ボイスフォルダパス", current_char.get("voice_dir", ""))
    current_char["prompt_text"] = st.text_area("サンプル音声の文字起こし（口調の学習用）", current_char.get("prompt_text", ""))
    
    st.subheader("シチュエーション別口調テンプレート")
    t_col1, t_col2, t_col3 = st.columns(3)
    current_char["response_templates"]["default"] = t_col1.text_area("通常時", current_char["response_templates"].get("default", ""))
    current_char["response_templates"]["whisper"] = t_col2.text_area("甘い時/囁き", current_char["response_templates"].get("whisper", ""))
    current_char["response_templates"]["stress"] = t_col3.text_area("不機嫌/圧", current_char["response_templates"].get("stress", ""))

    if st.form_submit_button("このキャラクターを保存にゃ！"):
        save_name = selected_file if selected_file.endswith(".json") else selected_file + ".json"
        with open(os.path.join(CHAR_DIR, save_name), "w", encoding="utf-8") as f:
            json.dump(current_char, f, indent=4, ensure_ascii=False)
        st.success(f"【{current_char['name']}】の全データを記録したよ！")
import streamlit as st
import json
import os
from PIL import Image

# --- フォルダ準備 ---
CHAR_DIR = "characters"
IMAGE_DIR = "images" # 画像保存用
os.makedirs(IMAGE_DIR, exist_ok=True)

# (中略：夢主設定などはそのまま)

# --- キャラクター設定セクション ---
with st.form("main_form"):
    # (中略：名前やMBTIの入力欄)

    st.subheader("ビジュアル設定")
    uploaded_file = st.file_uploader("推しの画像を選択（jpg/png）", type=['png', 'jpg', 'jpeg'])
    
    # 画像がアップロードされたら保存してパスを記録
    if uploaded_file is not None:
        img_path = os.path.join(IMAGE_DIR, f"{current_char['name']}_icon.png")
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        current_char["image_path"] = img_path
        st.image(img_path, caption="現在の設定画像", width=150)
    elif "image_path" in current_char and os.path.exists(current_char["image_path"]):
        st.image(current_char["image_path"], caption="設定済み画像", width=150)

    # (中略：保存ボタンなど)
    import streamlit as st
import json
import os
from PIL import Image

# --- ディレクトリ構成 ---
CHAR_DIR = "characters"
IMAGE_DIR = "images"
USER_DIR = "users"
for d in [CHAR_DIR, IMAGE_DIR, USER_DIR]:
    os.makedirs(d, exist_ok=True)

st.set_page_config(page_title="推し設定編集", layout="wide")

# --- 共通関数：JSON読み書き ---
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- サイドバー：自分設定 ---
with st.sidebar:
    st.header("👤 夢主設定")
    user_file = os.path.join(USER_DIR, "me.json")
    user_data = load_json(user_file) if os.path.exists(user_file) else {"name": "", "mbti": "INFP", "traits": "", "weakness": ""}
    
    with st.form("user_form"):
        user_data["name"] = st.text_input("あなたの名前", user_data["name"])
        user_data["mbti"] = st.text_input("あなたのMBTI", user_data["mbti"])
        user_data["traits"] = st.text_area("あなたの特徴", user_data["traits"])
        if st.form_submit_button("自分設定を保存"):
            save_json(user_file, user_data)
            st.success("保存完了にゃ！")

# --- メイン：キャラ編集 ---
st.title("🎭 キャラクター設定・変更")

char_files = [f for f in os.listdir(CHAR_DIR) if f.endswith(".json")]
mode = st.radio("作業を選択", ["既存キャラを修正", "新規キャラ作成"], horizontal=True)

# 編集対象のデータを準備
if mode == "既存キャラを修正" and char_files:
    target_file = st.selectbox("編集するキャラを選択", char_files)
    current_data = load_json(os.path.join(CHAR_DIR, target_file))
else:
    target_file = st.text_input("新規ファイル名 (例: oshi_b.json)")
    current_data = {
        "name": "", "age": 30, "sexuality": "男性", "mbti": "INTJ",
        "first_person": "俺", "second_person": "お前", "traits": "",
        "job": "", "hobby": "", "likes": "", "dislikes": "", "personality": "",
        "image_path": "", "voice_dir": "", "prompt_text": "",
        "response_templates": {"default": "", "whisper": "", "stress": ""}
    }

# --- 編集フォーム ---
with st.form("edit_form"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🖼️ ビジュアル")
        if current_data.get("image_path") and os.path.exists(current_data["image_path"]):
            st.image(current_data["image_path"], caption="現在の画像", width=150)
        uploaded_file = st.file_uploader("新しい画像を選択", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            img_path = os.path.join(IMAGE_DIR, f"{current_data['name']}_icon.png")
            with open(img_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            current_data["image_path"] = img_path
            st.image(img_path, caption="新しい画像", width=150)

    with col2:
        st.subheader("基本情報")
        current_data["name"] = st.text_input("名前", current_data.get("name", ""))
        current_data["age"] = st.number_input("年齢", value=current_data.get("age", 20))
        current_data["sexuality"] = st.text_input("性別/性自認", current_data.get("sexuality", "男性"))
        current_data["mbti"] = st.text_input("MBTI", current_data.get("mbti", "INTJ"))
        # (以下、他の入力欄も同様に配置)

    if st.form_submit_button("このキャラを保存"):
        save_name = target_file if target_file.endswith(".json") else target_file + ".json"
        save_json(os.path.join(CHAR_DIR, save_name), current_data)
        st.success(f"【{current_data['name']}】のデータを保存したよ！")
        import streamlit as st
import os

# --- フォルダ準備 ---
VOICE_BASE_DIR = "voice_samples"
os.makedirs(VOICE_BASE_DIR, exist_ok=True)

# (キャラクター編集フォーム内での実装例)
with st.form("edit_form"):
    # ...（前述の名前や性格設定などのコード）...

    st.subheader("🎤 ボイスサンプルの追加")
    
    # 1. 保存先のフォルダを確定（キャラ名ごとのフォルダ）
    char_voice_dir = os.path.join(VOICE_BASE_DIR, current_data["name"])
    os.makedirs(char_voice_dir, exist_ok=True)
    
    # 2. スマホから音声ファイルをアップロード
    uploaded_voice = st.file_uploader(
        "スマホから音声を選択・または録音をアップロードにゃ！", 
        type=["wav", "mp3", "m4a"],
        help="推しの綺麗な声をアップロードしてね"
    )

    # 3. アップロードされた際の処理
    if uploaded_voice is not None:
        # ファイル名を整理して保存
        voice_path = os.path.join(char_voice_dir, uploaded_voice.name)
        with open(voice_path, "wb") as f:
            f.write(uploaded_voice.getbuffer())
        
        # JSON側のパス設定も更新
        current_data["voice_sample"] = voice_path
        st.success(f"音声ファイル【{uploaded_voice.name}】を保存したにゃ！")
        
        # アップロードした音声をその場で確認再生
        st.audio(voice_path)

    # ...（保存ボタンなど）...
    import streamlit as st
import os

# --- 感情ラベルの定義 ---
EMOTION_LABELS = {
    "通常 (Normal)": "default",
    "囁き・官能 (Whisper)": "whisper",
    "不機嫌・圧 (Stress)": "stress"
}

# (キャラクター編集フォーム内、ボイスセクション)
st.subheader("🎤 ボイスサンプルの感情割り当て")

char_voice_dir = os.path.join("voice_samples", current_data["name"])
os.makedirs(char_voice_dir, exist_ok=True)

# 1. ファイルアップローダー
uploaded_voice = st.file_uploader(
    "ボイスファイルをアップロード", 
    type=["wav", "mp3", "m4a"]
)

if uploaded_voice is not None:
    # 2. どの感情として保存するか選択
    selected_label = st.radio(
        "この音声の『感情タイプ』を選んでにゃ：", 
        list(EMOTION_LABELS.keys()),
        horizontal=True
    )
    emotion_key = EMOTION_LABELS[selected_label]

    # 保存処理ボタン
    if st.button(f"{selected_label} として登録する"):
        # ファイル名を感情名に合わせて保存 (例: oshi_whisper.wav)
        file_ext = os.path.splitext(uploaded_voice.name)[1]
        save_filename = f"refer_{emotion_key}{file_ext}"
        voice_path = os.path.join(char_voice_dir, save_filename)
        
        with open(voice_path, "wb") as f:
            f.write(uploaded_voice.getbuffer())
        
        # JSONのemotionsパスを更新
        current_data["emotions"][emotion_key] = voice_path
        st.success(f"【{selected_label}】の音声を更新したよ！")
        st.audio(voice_path)

st.divider()

# 現在設定されている感情ボイスの確認
st.write("🎵 現在の登録状況")
cols = st.columns(3)
for i, (label, key) in enumerate(EMOTION_LABELS.items()):
    path = current_data["emotions"].get(key, "")
    if path and os.path.exists(path):
        cols[i].caption(label)
        cols[i].audio(path)
    else:
        cols[i].warning(f"{label} 未登録")

