from langdetect import detect

class DialogueParser:
    def __init__(self):
        self.speaker_markers = {
            'ja': {
                'alice': ['アリス', 'alice', 'Alice'],
                'bob': ['ボブ', 'bob', 'Bob']
            }
        }

    def detect_language(self, text):
        try:
            return detect(text)
        except:
            return 'ja'  # デフォルトは日本語

    def parse_dialogue(self, text):
        language = self.detect_language(text)
        lines = text.split('\n')
        dialogues = []
        
        current_speaker = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_speaker and current_text:
                    dialogues.append({
                        'speaker': current_speaker,
                        'text': ' '.join(current_text)
                    })
                    current_speaker = None
                    current_text = []
                continue

            # 話者の検出
            for speaker, markers in self.speaker_markers[language].items():
                if any(marker in line.lower() for marker in markers):
                    if current_speaker and current_text:
                        dialogues.append({
                            'speaker': current_speaker,
                            'text': ' '.join(current_text)
                        })
                    current_speaker = speaker
                    current_text = []
                    break

            if current_speaker:
                current_text.append(line)

        # 最後の会話を追加
        if current_speaker and current_text:
            dialogues.append({
                'speaker': current_speaker,
                'text': ' '.join(current_text)
            })

        return dialogues

    def parse(self, text):
        """テキストを会話形式にパース"""
        if not text or not text.strip():
            return []

        dialogues = []
        lines = text.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # "キャラクター名: セリフ" の形式をパース
            try:
                speaker, content = line.split(':', 1)
                speaker = speaker.strip()
                content = content.strip()

                if speaker and content:
                    dialogues.append({
                        'speaker': speaker.lower(),  # キャラクターIDは小文字で統一
                        'text': content
                    })
            except ValueError:
                continue  # 不正な形式の行はスキップ

        return dialogues 