import tkinter
import tkinter.font
import tkinter.ttk
import PIL.Image
import PIL.ImageTk
import pygame
import time
import os
from dictionary_processor import DictionaryProcessor
from language_processor import Translator
from gtts import gTTS, tts
import gtts.lang


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RESIZABLE = False
LOGO_ICON = "logo.ico"
LOGO_IMG = "logo.png"
SPEAKER_IMG = "speaker.png"
TITLE = "LinguaLuxe"
DARK_BG = "#2D2B2B"
BUTTON_BG = "#2AA0ED"
ENTRY_BG = "#1C1A1A"
FONT_COLOR = "#FFFFFF"
SMALL_FONT = {"family": "Consolas", "size": 12}
LARGE_FONT = {"family": "Consolas", "size": 18, "weight": "bold"}
HEADER_FONT = {"family": "Consolas", "size": 24, "weight": "bold"}


class App(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        # call parents constructor
        super().__init__(*args, **kwargs)

        # container
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # title, size, icon, resizable
        self.title(TITLE)
        self.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")

        if os.path.exists(LOGO_ICON):
            try:
                self.iconbitmap(os.path.abspath(LOGO_ICON))
            except Exception:
                pass

        self.resizable(RESIZABLE, RESIZABLE)

        # frames
        self.frames = {}

        # pages
        self.pages = [HomePage, DictionaryPage, TranslatorPage]

        # initialize frames
        for page in self.pages:
            frame = page(parent=container, controller=self)
            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # initially show home page
        self.show_frame(HomePage)

    # change frame
    def show_frame(self, page):
        # raise the frame
        frame = self.frames[page]
        frame.tkraise()


class HomePage(tkinter.Frame):

    def __init__(self, parent, controller):
        # call parent's constructor
        super().__init__(parent, bg=DARK_BG)

        # Logo
        self.logo_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(LOGO_IMG).resize((300, 200))
        )

        tkinter.Label(self, text="", image=self.logo_image, background=DARK_BG).pack(
            pady=150
        )

        # dictionary button
        tkinter.Button(
            self,
            text="Dictionary",
            command=lambda: controller.show_frame(DictionaryPage),
            bg=BUTTON_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            relief="flat",
            borderwidth=0,
        ).place(x=225, y=400, width=150, height=30)

        # translator button
        tkinter.Button(
            self,
            text="Translator",
            command=lambda: controller.show_frame(TranslatorPage),
            bg=BUTTON_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            relief="flat",
            borderwidth=0,
        ).place(x=425, y=400, width=150, height=30)


class DictionaryPage(tkinter.Frame):

    def __init__(self, parent, controller):
        # call parent's constructor
        super().__init__(parent, bg=DARK_BG)

        # logo
        self.logo_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(LOGO_IMG).resize((180, 120))
        )

        tkinter.Label(self, text="", image=self.logo_image, background=DARK_BG).place(
            x=100, y=80
        )

        # input label
        tkinter.Label(
            self,
            text="Input",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        ).place(x=40, y=250)

        # input entry
        self.input_entry = tkinter.Entry(
            self,
            bg=ENTRY_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            relief="flat",
            borderwidth=0,
        )
        self.input_entry.place(x=100, y=250, width=150, height=27)

        # text label
        self.text_label = tkinter.Label(
            self,
            text="",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=HEADER_FONT["family"],
                size=HEADER_FONT["size"],
                weight=HEADER_FONT["weight"],
            ),
        )
        self.text_label.place(x=350, y=50)

        # scrollable area
        canvas = tkinter.Canvas(
            self, bg=DARK_BG, highlightthickness=0, relief="flat", borderwidth=0
        )
        canvas.place(x=350, y=100, width=420, height=470)

        scrollbar = tkinter.Scrollbar(
            self,
            orient="vertical",
            command=canvas.yview,
            width=0,
            relief="flat",
            borderwidth=0,
        )
        canvas.config(yscrollcommand=scrollbar.set)
        scrollbar.place(x=770, y=100, height=470)

        # scrollable frame within canvas
        self.scrollable_frame = tkinter.Frame(
            canvas, bg=DARK_BG, relief="flat", borderwidth=0
        )
        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.canvas_frame = canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        # make scrollbar functional
        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"),
        )

        # call dictionary
        def call_dictionary():
            text = self.input_entry.get().strip()

            try:
                result = get_result(text)

            except ValueError:
                pass

            else:
                show_result(text, result)

        # show result
        def show_result(text: str, result: dict[str, list[str]]) -> None:
            # change text label
            self.text_label.config(text=text.title())

            # clear previous labels
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            # insert new labels
            current_row = 0

            for key in list(result.keys()):
                # skip if no result
                if len(result[key]) == 0:
                    continue

                # key label
                tkinter.Label(
                    self.scrollable_frame,
                    text=key.replace("_", " ").title(),
                    bg=DARK_BG,
                    fg=FONT_COLOR,
                    font=tkinter.font.Font(
                        family=LARGE_FONT["family"],
                        size=LARGE_FONT["size"],
                        weight=LARGE_FONT["weight"],
                    ),
                    wraplength=420,
                ).grid(row=current_row, column=0, sticky="w", pady=5)

                # update row
                current_row += 1

                # separator
                tkinter.ttk.Separator(self.scrollable_frame, orient="horizontal").grid(
                    row=current_row, column=0, sticky="ew", pady=5
                )

                # update row
                current_row += 1

                # value labels
                for value in result[key]:
                    tkinter.Label(
                        self.scrollable_frame,
                        text=f"⦾ {value}",
                        bg=DARK_BG,
                        fg=FONT_COLOR,
                        font=tkinter.font.Font(
                            family=SMALL_FONT["family"], size=SMALL_FONT["size"]
                        ),
                        wraplength=420,
                        justify="left",
                        anchor="w",
                    ).grid(row=current_row, column=0, sticky="w", pady=2)

                    # update row
                    current_row += 1

        # search button
        tkinter.Button(
            self,
            text="Search",
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            fg=FONT_COLOR,
            bg=BUTTON_BG,
            command=call_dictionary,
            relief="flat",
            borderwidth=0,
        ).place(x=100, y=300, width=80, height=27)

        # home button
        tkinter.Button(
            self,
            text="Return",
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            fg=FONT_COLOR,
            bg=BUTTON_BG,
            command=lambda: controller.show_frame(HomePage),
            relief="flat",
            borderwidth=0,
        ).place(x=30, y=550, width=80, height=27)


class TranslatorPage(tkinter.Frame):

    def __init__(self, parent, controller):
        # call paren's constructor
        super().__init__(parent, bg=DARK_BG)

        # initialize mixer
        pygame.mixer.init()

        # logo
        self.logo_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(LOGO_IMG).resize((180, 120))
        )

        tkinter.Label(self, text="", image=self.logo_image, background=DARK_BG).place(
            x=310, y=40
        )

        # input label
        tkinter.Label(
            self,
            text="Input",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        ).place(x=35, y=200)

        # input entry
        self.input_entry = tkinter.Text(
            self,
            wrap=tkinter.WORD,
            bg=ENTRY_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            relief="flat",
            borderwidth=0,
        )
        self.input_entry.place(x=100, y=200, width=200, height=200)

        # home button
        tkinter.Button(
            self,
            text="Return",
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            fg=FONT_COLOR,
            bg=BUTTON_BG,
            command=lambda: controller.show_frame(HomePage),
            relief="flat",
            borderwidth=0,
        ).place(x=30, y=550, width=80, height=27)

        # source label
        tkinter.Label(
            self,
            text="Translate from",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        ).place(x=35, y=420)

        # get supported languages
        self.supported_languages = get_supported_languages()
        self.supported_languages_list = [
            lang.strip().title() for lang in self.supported_languages
        ]

        # source language
        self.source_language = tkinter.StringVar(self)
        self.source_language.set("Auto")

        # source language option menu
        tkinter.ttk.OptionMenu(
            self, self.source_language, "Auto", "Auto", *self.supported_languages_list
        ).place(x=100, y=450, width=150)

        # detected source label
        self.detected_source_label = tkinter.Label(
            self,
            text="",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        )
        self.detected_source_label.place(x=40, y=480)

        # audio image
        self.audio_image = PIL.ImageTk.PhotoImage(
            PIL.Image.open(SPEAKER_IMG).resize((40, 40))
        )

        # play input audio
        def play_input_audio():
            # get input text
            text = self.input_entry.get("1.0", "end-1c").strip()

            if not text:
                return

            # get language
            language = self.source_language.get()

            if language == "Auto":
                language = detect_language(text)

                # get supported languages
                inverse_languages = {v: k for k, v in self.supported_languages.items()}

                # update detected source
                self.detected_source_label.config(
                    text=f"Detected language: {inverse_languages[language].title()}"
                )

            else:
                language = self.supported_languages[language.lower()]

                # remove previous text
                self.detected_source_label.config(text="")

            # get supported languages
            supported_languages = gtts.lang.tts_langs()

            if language not in list(supported_languages.keys()):
                return

            # generate speech
            generate_speech(text, language).save("input.mp3")

            # play audio
            pygame.mixer.music.load("input.mp3")
            pygame.mixer.music.play()

            # wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # unload music
            pygame.mixer.music.unload()

        # input audio
        tkinter.Button(
            self,
            text="",
            image=self.audio_image,
            bg=DARK_BG,
            command=play_input_audio,
            relief="flat",
            borderwidth=0,
        ).place(x=315, y=200)

        # translate function
        def get_translation():
            # get selections
            source_language = self.source_language.get()
            destination_language = self.destination_language.get()

            # get input
            text = self.input_entry.get("1.0", "end-1c").strip()

            # clear output text
            self.output_entry.config(state="normal")
            self.output_entry.delete("1.0", tkinter.END)

            # get translation
            translated_text = translate(
                text, self.supported_languages[destination_language.lower()]
            ).strip()

            # update output text
            self.output_entry.insert(tkinter.END, translated_text)
            self.output_entry.config(state="disabled")

            # if source language is auto, detect source
            if source_language == "Auto" and text != "":
                # detect language
                detected_language = detect_language(text)

                # get supported languages
                inverse_languages = {v: k for k, v in self.supported_languages.items()}

                # update detected source
                self.detected_source_label.config(
                    text=f"Detected language: {inverse_languages[detected_language].title()}"
                )

            # remove previous text
            else:
                self.detected_source_label.config(text="")

        # translate button
        tkinter.Button(
            self,
            text="Translate",
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            bg=BUTTON_BG,
            fg=FONT_COLOR,
            relief="flat",
            borderwidth=0,
            command=get_translation,
        ).place(x=345, y=520, width=110)

        # output label
        tkinter.Label(
            self,
            text="Output",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        ).place(x=435, y=200)

        # output entry
        self.output_entry = tkinter.Text(
            self,
            wrap=tkinter.WORD,
            bg=ENTRY_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
            relief="flat",
            borderwidth=0,
            state="disabled",
        )
        self.output_entry.place(x=500, y=200, width=200, height=200)

        # destination label
        tkinter.Label(
            self,
            text="Translate to",
            background=DARK_BG,
            fg=FONT_COLOR,
            font=tkinter.font.Font(
                family=SMALL_FONT["family"], size=SMALL_FONT["size"]
            ),
        ).place(x=435, y=420)

        # destination language
        self.destination_language = tkinter.StringVar(self)
        self.destination_language_list = []
        self.destination_language.set("English")

        # destination language option menu
        tkinter.ttk.OptionMenu(
            self,
            self.destination_language,
            "English",
            *self.supported_languages_list,
        ).place(x=500, y=450, width=150)

        # play output audio
        def play_output_audio():
            # get input text
            text = self.output_entry.get("1.0", "end-1c").strip()

            if not text:
                return

            # get language
            language = self.supported_languages[self.destination_language.get().lower()]

            # get supported languages
            supported_languages = gtts.lang.tts_langs()

            if language not in list(supported_languages.keys()):
                return

            # generate speech
            generate_speech(text, language).save("output.mp3")

            # play audio
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

            # wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # unload music
            pygame.mixer.music.unload()

        # input audio
        tkinter.Button(
            self,
            text="",
            image=self.audio_image,
            bg=DARK_BG,
            command=play_output_audio,
            relief="flat",
            borderwidth=0,
        ).place(x=715, y=200)


def main():
    App().mainloop()


def generate_speech(text: str = "", lang: str = "en", slow: bool = False) -> tts.gTTS:
    if text == "":
        raise ValueError

    return gTTS(text=text, lang=lang, slow=slow)


def detect_language(text: str = "") -> str:
    if text == "":
        raise ValueError

    return Translator.detect_language(text.strip().lower())


def get_supported_languages() -> dict[str, str]:
    return Translator.get_supported_languages()


def translate(text: str = "", lang: str = "en") -> str:
    if text == "":
        raise ValueError

    return Translator.translate(text, lang)


def get_result(text: str = "", lang: str = "en") -> dict[str, list[str]]:
    if text == "":
        raise ValueError

    return {
        **get_meaning(text, lang),
        **get_synonym(text, lang),
        **get_antonym(text, lang),
    }


def print_result(result: dict[str, list[str]]) -> None:
    for key in list(result.keys()):
        if len(result[key]) > 0:
            print(f"{key.replace("_", " ").title()}:")

            for value in result[key]:
                print("\t⦾", value)


def get_meaning(text: str = "", lang: str = "en") -> dict[str, list[str]]:
    if text == "":
        raise ValueError

    if detect_language(text) != "en":
        text = translate(text)

    return DictionaryProcessor.get_meaning(text.strip().lower(), lang.strip().lower())


def get_synonym(text: str = "", lang: str = "en") -> dict[str, list[str]]:
    if text == "":
        raise ValueError

    if detect_language(text) != "en":
        text = translate(text)

    return DictionaryProcessor.get_synonym(text.strip().lower(), lang.strip().lower())


def get_antonym(text: str = "", lang: str = "en") -> dict[str, list[str]]:
    if text == "":
        raise ValueError

    if detect_language(text) != "en":
        text = translate(text)

    return DictionaryProcessor.get_antonym(text.strip().lower(), lang.strip().lower())


if __name__ == "__main__":
    main()
