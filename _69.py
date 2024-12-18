import os
import time
import pyautogui
import pyperclip
from colorama import init, Fore, Style
import random
import threading
from pynput import keyboard

# Initialize colorama for styled text
init(autoreset=True)
pyautogui.FAILSAFE = False


class TurboTyper:
    VERSION = "1.2"
    
    def __init__(self):
        self.words_file = r"C:\Users\a\source\repos\69\words1.txt"
        self.typing_speed = 0.01
        self.min_speed = 0.001
        self.max_speed = 1.0
        self.is_typing = False
        self.words = []
        self.stop_event = threading.Event()
        self.current_keybind = 'p'
        self.current_mode = '1'  # Default to Sequential Typing
        self.current_index = 0  # Used for sequential mode
        self.used_indices = set()  # Tracks used words in Random Typing
        self.target_user = None  # Victim username

    def print_banner(self):
        banner_text = f"""{Fore.MAGENTA}
                                (@mtflt1)
                     ███╗   ███╗████████╗███████╗██╗  ████████╗
                     ████╗ ████║╚══██╔══╝██╔════╝██║  ╚══██╔══╝
                     ██╔████╔██║   ██║   █████╗  ██║     ██║   
                     ██║╚██╔╝██║   ██║   ██╔══╝  ██║     ██║   
                     ██║ ╚═╝ ██║   ██║   ██║     ███████╗██║   
                     ╚═╝     ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝   
{Style.RESET_ALL}
{Fore.CYAN}{' Version ' + self.VERSION + ' | Developer Edition '.center(80)}{Style.RESET_ALL}
"""
        print(banner_text)

    def load_words(self):
        encodings = ['utf-8-sig', 'utf-16', 'cp1256', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(self.words_file, 'r', encoding=encoding) as file:
                    self.words = [line.strip() for line in file.readlines() if line.strip()]
                if self.words:
                    print(f"{Fore.GREEN}[+] Loaded {len(self.words)} words using {encoding}{Style.RESET_ALL}")
                    return
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        print(f"{Fore.RED}[!] Failed to load words. Check the file.{Style.RESET_ALL}")
        self.words = ["Test word"]

    def turbo_type(self, text):
        try:
            saved_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            
            # Paste and detect tags
            pyautogui.hotkey('ctrl', 'v')
            if '@' in text:  # Tag detected
                time.sleep(0.1)  # Delay for tag processing
                pyautogui.press('enter')  # First enter
                pyautogui.press('enter')  # Second enter
            else:
                pyautogui.press('enter')
                
            pyperclip.copy(saved_clipboard)  # Restore original clipboard
            time.sleep(self.typing_speed)
        except Exception as e:
            print(f"{Fore.RED}[!] Error during typing: {e}{Style.RESET_ALL}")

    def start_typing(self, mode):
        if mode == '1':  # Sequential Typing
            while not self.stop_event.is_set():
                if self.current_index >= len(self.words):
                    print(f"{Fore.YELLOW}[!] All words in the file have been typed. Stopping.{Style.RESET_ALL}")
                    self.stop_event.set()
                    self.is_typing = False
                    break
                text = self.apply_target(self.words[self.current_index])
                self.turbo_type(text)
                self.current_index += 1
        elif mode == '2':  # Random Typing
            while not self.stop_event.is_set():
                if len(self.used_indices) >= len(self.words):
                    self.used_indices.clear()  # Reset when all words have been used
                available_indices = set(range(len(self.words))) - self.used_indices
                idx = random.choice(list(available_indices))
                self.used_indices.add(idx)
                text = self.apply_target(self.words[idx])
                self.turbo_type(text)
        elif mode == '3':  # Victim Mode
            while not self.stop_event.is_set():
                if self.current_index >= len(self.words):
                    print(f"{Fore.YELLOW}[!] All words with the target user have been typed. Stopping.{Style.RESET_ALL}")
                    self.stop_event.set()
                    self.is_typing = False
                    break
                text = self.apply_target(self.words[self.current_index])
                self.turbo_type(text)
                self.current_index += 1

    def apply_target(self, text):
        if self.target_user:
            return f"@{self.target_user} {text}"
        return text

    def on_key_press(self, key):
        try:
            key_str = str(key).replace("'", "")  # Remove quotes for keys like letters or Arabic characters
            if key_str == self.current_keybind:
                if self.is_typing:
                    self.stop_event.set()
                    self.is_typing = False
                    print(f"{Fore.YELLOW}[■] Stopped typing.{Style.RESET_ALL}")
                else:
                    self.stop_event.clear()
                    threading.Thread(target=self.start_typing, args=(self.current_mode,), daemon=True).start()
                    self.is_typing = True
                    print(f"{Fore.GREEN}[▶] Started typing.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

    def set_target_user(self):
        username = input(f"{Fore.GREEN}Enter the target username (or press Enter to disable): {Style.RESET_ALL}").strip()
        if username:
            self.target_user = username
            print(f"{Fore.GREEN}[+] Target username set to: @{self.target_user}{Style.RESET_ALL}")
        else:
            self.target_user = None
            print(f"{Fore.YELLOW}[!] Target username disabled.{Style.RESET_ALL}")

    def set_custom_speed(self):
        try:
            speed = float(input(f"{Fore.GREEN}Enter typing speed (0.001 - 1.0): {Style.RESET_ALL}"))
            if self.min_speed <= speed <= self.max_speed:
                self.typing_speed = speed
                print(f"{Fore.GREEN}[+] Speed set to: {speed}s{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Speed must be between {self.min_speed} and {self.max_speed}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    def set_keybind(self):
        print(f"{Fore.YELLOW}Press a key for your new keybind (Arabic, special characters allowed).{Style.RESET_ALL}")
        with keyboard.Listener(on_press=self.validate_keybind) as listener:
            listener.join()

    def validate_keybind(self, key):
        try:
            key_str = str(key).replace("'", "")  # Handle any key input
            if key_str:
                self.current_keybind = key_str
                print(f"{Fore.GREEN}[+] Keybind set to '{self.current_keybind}'{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}[!] Invalid key. Please try again.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error setting keybind: {e}{Style.RESET_ALL}")
        return False

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.print_banner()
        self.load_words()
        keyboard.Listener(on_press=self.on_key_press).start()

        print(f"""
{Fore.CYAN}
                            [1] Sequential Typing
                            [2] Random Typing
                            [3] Target a User (Victim Mode)
                            [4] Set Custom Speed
                            [5] Set Keybind
                            [6] Exit
{Style.RESET_ALL}
""")
        
        while True:
            choice = input(f"{Fore.GREEN}Select option: {Style.RESET_ALL}").strip()
            if choice in ['1', '2', '3']:
                self.current_mode = choice
                self.current_index = 0  # Reset index for Sequential Typing
                if choice == '3':
                    self.set_target_user()
            elif choice == '4':
                self.set_custom_speed()
            elif choice == '5':
                self.set_keybind()
            elif choice == '6':
                print(f"{Fore.YELLOW}[!] Exiting...{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}[!] Invalid option.{Style.RESET_ALL}")


if __name__ == "__main__":
    typer = TurboTyper()
    typer.run()
