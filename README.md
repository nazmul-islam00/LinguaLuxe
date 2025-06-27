# LinguaLuxe



LinguaLuxe is my CS50P final project, an application built using tkinter. This works as a dictionary and a translator(with support for pronunciations).



## Getting Started


This project uses external modules. At first install the modules using the following command:
```
pip install pytest pygame gtts pillow langid PyMultiDictionary deep_translator
```

Now go ahead and run the following command:
```
python project.py
```


## About


In this project, I used two separate classes ```DictionaryProcessor``` and ```Translator``` for the calls to the external modules. For the text-to-speech part, I used the Google Text to Speech module ```gtts```.


The project has three pages which have been implemented as subclasses of ```tkinter.Frame```. These classes are ```HomePage```, ```DictionaryPage``` and ```TranslatorPage```. All these classes were added to the ```App``` class which extends the ```tkinter.Tk``` class. 


The ```DictionaryProcessor``` class provides the following functionalities:

* getting the part of speech
* getting the meaning
* getting the synonyms
* getting the antonyms

All these use the ```PyMultiDictionary``` module.

The ```Translator``` class serves the following purposes:

* detecting language (using ```langid```)
* translating to different languages (using ```deep_translator```)


The ```App``` class uses the other three subclasses and adds them as frames. Using the ```show_frame``` function, it raises the corresponding frame according to commands.

The ```HomePage``` has buttons to redirect to the ```DictionaryPage``` and ```TranslatorPage```. 

The ```DicionaryPage``` provides an input box. Upon clicking the search button, it calls the ```DictionaryProcessor``` and shows the results in a scrollable frame beside.

The ```TranslatorPage``` also provides and input box. It gives option-menus to choose from which language and to which language you want to translate. If the input language is set to ```Auto```, it detects the source language using ```langid``` and displays it below. The ```Translate``` button shows the translated text in the output box. The input and output text can also be heard by using the audio icons beside them. These use the ```gtts``` module to generate the speech.



#### Youtube: https://youtu.be/cMhNzBpDt10
