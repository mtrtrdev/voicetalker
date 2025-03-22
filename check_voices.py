import win32com.client
import winreg

def check_available_voices():
    # SAPIを使用して音声を確認
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    
    print("SAPIで利用可能な音声:")
    for voice in voices:
        print(f"\n音声:")
        print(f"説明: {voice.GetDescription()}")
        print("---")

    # レジストリから音声を確認
    print("\nレジストリに登録されている音声:")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Speech\Voices\Tokens")
        i = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    description = winreg.QueryValueEx(subkey, "")[0]
                    print(f"\n音声: {description}")
                    print(f"キー: {subkey_name}")
                except:
                    pass
                winreg.CloseKey(subkey)
                i += 1
            except WindowsError:
                break
        winreg.CloseKey(key)
    except Exception as e:
        print(f"レジストリの読み取りエラー: {e}")

if __name__ == "__main__":
    check_available_voices() 