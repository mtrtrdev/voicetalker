from gtts import gTTS
from io import BytesIO
import json
import librosa
import soundfile as sf
import numpy as np
import logging
from scipy import signal

# ログ設定をより詳細に
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TTSEngine:
    def __init__(self):
        try:
            self.characters = self._load_characters()
            self.sample_rate = 44100
            logger.info("TTSEngine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTSEngine: {e}")
            raise

    def _load_characters(self):
        try:
            with open('characters/config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"Loaded characters: {list(config['characters'].keys())}")
                return config['characters']
        except Exception as e:
            logger.error(f"Failed to load characters config: {e}")
            raise

    def _adjust_volume(self, y, gain_db):
        """音量をデシベル単位で調整"""
        if gain_db == 0:
            return y
        factor = np.power(10.0, gain_db / 20.0)
        return y * factor

    def _enhance_bass(self, y, bass_boost=0):
        """低音を強調"""
        if bass_boost == 0:
            return y

        # ローパスフィルタの設定
        cutoff = 200  # カットオフ周波数
        nyquist = self.sample_rate // 2
        normal_cutoff = cutoff / nyquist
        order = 4

        # バターワースフィルタの作成
        b, a = signal.butter(order, normal_cutoff, btype='lowpass')
        
        # 低周波成分の抽出
        bass = signal.filtfilt(b, a, y)
        
        # 低周波成分の強調
        boost_factor = np.power(10.0, bass_boost / 20.0)
        enhanced = y + (bass * (boost_factor - 1))
        
        return enhanced

    def _process_audio(self, y, sr, character):
        """音声の加工（ピッチ、速度、音量、低音強調）"""
        try:
            logger.info(f"Processing audio with parameters: {character}")
            
            # 速度調整
            y = librosa.effects.time_stretch(y, rate=character.get('speed_rate', 1.0))
            logger.debug("Speed adjustment completed")
            
            # ピッチ調整
            pitch_steps = character.get('pitch_steps', 0)
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_steps)
            logger.debug("Pitch adjustment completed")
            
            # 音量調整
            if character.get('volume_gain_db', 0) != 0:
                factor = np.power(10.0, character.get('volume_gain_db', 0) / 20.0)
                y = y * factor
                logger.debug("Volume adjustment completed")
            
            # 低音強調
            if character.get('bass_boost', 0) != 0:
                cutoff = 200
                nyquist = sr // 2
                normal_cutoff = cutoff / nyquist
                b, a = signal.butter(4, normal_cutoff, btype='lowpass')
                bass = signal.filtfilt(b, a, y)
                boost_factor = np.power(10.0, character.get('bass_boost', 0) / 20.0)
                y = y + (bass * (boost_factor - 1))
                logger.debug("Bass boost completed")
            
            return y
            
        except Exception as e:
            logger.error(f"Error in audio processing: {e}")
            raise

    def _make_text_natural(self, text):
        """句読点で自然なポーズを入れる"""
        return text.replace("、", "、…").replace("。", "。…")

    def generate_all_speeches(self, dialogues, selected_characters):
        if not dialogues or not selected_characters:
            logger.warning("No dialogues or selected characters provided")
            return None

        try:
            logger.info(f"Starting speech generation for {len(dialogues)} dialogues")
            logger.info(f"Selected characters: {list(selected_characters.keys())}")
            
            all_audio_arrays = []
            
            for dialogue in dialogues:
                speaker = dialogue['speaker']
                text = dialogue['text'].strip()
                
                logger.info(f"Processing dialogue - Speaker: {speaker}, Text: {text}")
                
                if speaker in selected_characters and text:
                    character = selected_characters[speaker]
                    
                    # 音声生成
                    try:
                        tts = gTTS(text=f"{text}。。。", lang=character['language'])
                        temp_buffer = BytesIO()
                        tts.write_to_fp(temp_buffer)
                        temp_buffer.seek(0)
                        logger.info(f"Generated base audio for {speaker}")
                        
                        # 音声読み込みと加工
                        y, sr = librosa.load(temp_buffer, sr=self.sample_rate)
                        y = self._process_audio(y, sr, character)
                        
                        all_audio_arrays.append(y)
                        logger.info(f"Successfully processed audio for {speaker}")
                        
                    except Exception as e:
                        logger.error(f"Error generating speech for {speaker}: {e}")
                        continue
                else:
                    logger.warning(f"Skipping dialogue - Invalid speaker or empty text: {speaker}")
            
            if all_audio_arrays:
                # 音声の結合
                combined_audio = np.concatenate(all_audio_arrays)
                
                # 音声の正規化
                max_val = np.max(np.abs(combined_audio))
                if max_val > 1.0:
                    combined_audio = combined_audio / max_val
                    logger.info("Audio normalized to prevent clipping")
                
                # WAVファイルとして保存
                output = BytesIO()
                sf.write(output, combined_audio, self.sample_rate, format='wav')
                output.seek(0)
                logger.info("All audio combined successfully")
                return output.getvalue()
            
            logger.warning("No audio was generated")
            return None

        except Exception as e:
            logger.error(f"Error in generate_all_speeches: {e}")
            return None
