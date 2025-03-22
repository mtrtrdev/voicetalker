# VoiceTalker

[English](README_EN.md) | 日本語

テキストベースの会話を、キャラクターごとに異なる声で音声化するWebアプリケーション

## 機能

- テキストから会話音声を生成
- キャラクターごとに異なる声の設定が可能
- 音声パラメータのリアルタイム調整と試聴
- 複数キャラクターの会話を1つの音声ファイルとして生成

## デモ

![VoiceTalker Demo](docs/images/demo.gif)

## インストール

1. リポジトリをクローン：
   ```bash
   git clone https://github.com/[username]/voicetalker.git
   cd voicetalker
   ```

2. 必要なパッケージをインストール：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. アプリケーションの起動：
   ```bash
   streamlit run app.py
   ```

2. ブラウザで開かれるアプリケーションにアクセス

### 会話生成

1. サイドバーの「会話生成」を選択
2. 使用するキャラクターをチェックボックスで選択
3. 以下の形式で会話テキストを入力：
   ```
   アリス: こんにちは！
   ボブ: やあ、アリス。
   ```
4. 「音声生成」ボタンをクリックして音声を生成

### 声の設定

1. サイドバーの「声の設定」を選択
2. 調整したいキャラクターを選択
3. パラメータを調整：
   - 話速（0.5～1.5）: 1.0が標準速度
   - 声の高さ（-12～12）: 0が標準の高さ
   - 音量（-20～20 dB）: 0が標準音量
   - 声の太さ（0～12）: 値が大きいほど低音が強調
4. テスト用テキストを入力して音声を確認

## パラメータの説明

### 音声設定パラメータ

- `speed_rate`: 話速
  - 1.0: 標準速度
  - >1.0: より速く
  - <1.0: より遅く

- `pitch_steps`: 声の高さ
  - 0: 標準の高さ
  - 正の値: より高く
  - 負の値: より低く

- `volume_gain_db`: 音量（デシベル）
  - 0: 標準音量
  - 正の値: より大きく
  - 負の値: より小さく

- `bass_boost`: 声の太さ
  - 0: 標準
  - 値が大きいほど低音が強調

## 開発環境

- Python 3.9+
- Streamlit 1.32.0
- gTTS 2.5.1
- その他の依存関係は`requirements.txt`を参照

## 注意事項

- インターネット接続が必要です（Google Text-to-Speech APIを使用）
- 音声生成には少し時間がかかる場合があります
- 生成された音声は一時的なものでサーバーには保存されません

## ライセンス

[MIT License](LICENSE)

## 作者

[Your Name]

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成：
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. 変更をコミット：
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. ブランチにプッシュ：
   ```bash
   git push origin feature/amazing-feature
   ```
5. プルリクエストを作成

## 謝辞

- [Google Text-to-Speech](https://cloud.google.com/text-to-speech) - 基本的な音声合成に使用
- [Streamlit](https://streamlit.io/) - Webインターフェースの構築に使用 