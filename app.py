"""
VoiceTalker - テキストから会話音声を生成するアプリケーション

このアプリケーションは、テキストベースの会話を音声に変換し、
キャラクターごとに異なる声で出力することができます。

使用方法:
1. サイドバーの「ページ選択」から目的の機能を選択します
   - 会話生成: 会話テキストから音声を生成
   - 声の設定: キャラクターの声のパラメータを調整

2. 会話生成ページ:
   - キャラクターを選択（複数選択可能）
   - 会話テキストを入力（形式: "キャラクター名: セリフ"）
   - 「音声生成」ボタンをクリックして音声を生成

3. 声の設定ページ:
   - キャラクターを選択
   - 各パラメータを調整（話速、声の高さ、音量、声の太さ）
   - テスト用テキストを入力して音声を確認
   - 設定をJSONとしてコピーしてconfig.jsonに反映可能
"""

import streamlit as st
from tts_engine import TTSEngine
from dialogue_parser import DialogueParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_voice_settings_form(character):
    """音声設定フォームの作成"""
    with st.form(key='voice_settings_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("名前", character['name'])
            language = st.selectbox("言語", ['ja', 'en'], 
                                  index=0 if character['language'] == 'ja' else 1)
            
            speed_rate = st.slider(
                "話速", 
                min_value=0.5,
                max_value=1.5,
                value=float(character.get('speed_rate', 1.0)),
                step=0.05,
                help="1.0が標準速度。大きいほど早く話します。"
            )
            
            pitch_steps = st.slider(
                "声の高さ",
                min_value=-12,
                max_value=12,
                value=int(character.get('pitch_steps', 0)),
                step=1,
                help="0が標準の高さ。負の値で低く、正の値で高くなります。"
            )
        
        with col2:
            volume_gain_db = st.slider(
                "音量",
                min_value=-20,
                max_value=20,
                value=int(character.get('volume_gain_db', 0)),
                step=1,
                help="0が標準音量。単位はデシベル(dB)。"
            )
            
            bass_boost = st.slider(
                "声の太さ",
                min_value=0,
                max_value=12,
                value=int(character.get('bass_boost', 0)),
                step=1,
                help="0が標準。大きいほど低音が強調されます。"
            )
            
            description = st.text_area("説明", character['description'])

        test_text = st.text_input("テスト用テキスト", "これはテスト用の音声です。")
        submit_button = st.form_submit_button("設定を適用")

        return submit_button, {
            "name": name,
            "language": language,
            "speed_rate": speed_rate,
            "pitch_steps": pitch_steps,
            "volume_gain_db": volume_gain_db,
            "bass_boost": bass_boost,
            "description": description
        }, test_text

def generate_test_audio(tts_engine, character_id, character_settings, test_text):
    """テスト音声の生成"""
    test_dialogue = [{
        "speaker": character_id,
        "text": test_text
    }]
    
    test_characters = {character_id: character_settings}
    return tts_engine.generate_all_speeches(test_dialogue, test_characters)

def display_json_settings(name, settings):
    """設定のJSON表示"""
    json_template = f"""{{
    "{name}": {{
        "name": "{name}",
        "language": "{settings['language']}",
        "speed_rate": {settings['speed_rate']},
        "pitch_steps": {settings['pitch_steps']},
        "volume_gain_db": {settings['volume_gain_db']},
        "bass_boost": {settings['bass_boost']},
        "description": "{settings['description']}"
    }}
}}"""
    st.code(json_template, language='json')

def voice_settings_page():
    """声の設定ページ"""
    st.title("声のパラメータ設定")
    
    st.markdown("""
    ### 📝 概要
    キャラクターの声のパラメータを調整し、試聴できます。
    良い設定が見つかったら、表示されるJSONをコピーしてconfig.jsonに反映できます。

    ### 🎯 使い方
    1. キャラクターを選択
    2. 各パラメータを調整
        - 話速: 1.0が標準（大きいほど早く）
        - 声の高さ: 0が標準（負の値で低く、正の値で高く）
        - 音量: 0が標準（デシベル単位）
        - 声の太さ: 0が標準（大きいほど低音が強調）
    3. テスト用テキストを入力して音声を確認
    4. 良い設定ができたらJSONをコピー
    """)
    
    st.divider()
    
    tts_engine = TTSEngine()
    characters = tts_engine.characters
    
    character_id = st.selectbox(
        "キャラクターを選択",
        list(characters.keys()),
        format_func=lambda x: characters[x]['name']
    )
    
    submit_button, new_settings, test_text = create_voice_settings_form(characters[character_id])

    if submit_button:
        audio_data = generate_test_audio(tts_engine, character_id, new_settings, test_text)
        if audio_data:
            st.audio(audio_data, format='audio/wav')
            display_json_settings(new_settings['name'], new_settings)
        else:
            st.error("音声の生成に失敗しました。")

def conversation_page():
    """会話生成ページ"""
    st.title("VoiceTalker")
    
    st.markdown("""
    ### 📝 概要
    テキストで入力した会話を、選択したキャラクターの声で再生します。
    複数のキャラクターの会話を1つの音声ファイルとして生成できます。

    ### 🎯 使い方
    1. サイドバーでキャラクターを選択（複数選択可）
    2. 以下の形式で会話テキストを入力：
    """)
    
    st.code("""太郎: こんにちは！
花子: やあ、太郎。
太郎: 今日はいい天気ですね。
花子: そうですね。""", language="text")
    
    st.markdown("""
    3. 「音声生成」ボタンをクリックして音声を生成
    4. 生成された音声を再生して確認
    """)
    
    st.divider()
    
    tts_engine = TTSEngine()
    
    st.sidebar.header("キャラクター選択")
    selected_characters = {}
    for char_id, char in tts_engine.characters.items():
        if st.sidebar.checkbox(f"{char['name']}", value=True):
            selected_characters[char_id] = char

    st.markdown("""
    ### 入力形式:
    ```
    太郎: こんにちは！
    花子: やあ、太郎。
    ```
    """)
    
    input_text = st.text_area("会話テキストを入力してください:", height=200)
    
    if st.button("音声生成", disabled=not input_text.strip()):
        if input_text.strip():
            parser = DialogueParser()
            dialogues = parser.parse(input_text)
            
            if dialogues:
                audio_data = tts_engine.generate_all_speeches(dialogues, selected_characters)
                if audio_data:
                    st.audio(audio_data, format='audio/wav')
                    st.success("音声が生成されました！")
                else:
                    st.warning("音声の生成中にエラーが発生しました。")
            else:
                st.warning("有効な会話が見つかりませんでした。入力形式を確認してください。")

def main():
    """メインアプリケーション"""
    with st.sidebar:
        st.title("🎤 VoiceTalker")
        st.markdown("""
        テキストから会話音声を生成するアプリケーション
        
        ### 🔍 機能
        - 会話生成: テキストから音声を作成
        - 声の設定: キャラクターの声を調整
        """)
        
        st.divider()
        
        page = st.radio("ページ選択", ["会話生成", "声の設定"])
    
    if page == "会話生成":
        conversation_page()
    else:
        voice_settings_page()

if __name__ == "__main__":
    main() 