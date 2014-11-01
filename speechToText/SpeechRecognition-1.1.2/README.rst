Google Speech Recognition
=========================

.. image:: https://pypip.in/download/SpeechRecognition/badge.svg
    :target: https://pypi.python.org/pypi/SpeechRecognition/
    :alt: Downloads

.. image:: https://pypip.in/version/SpeechRecognition/badge.svg
    :target: https://pypi.python.org/pypi/SpeechRecognition/
    :alt: Latest Version

.. image:: https://pypip.in/status/SpeechRecognition/badge.svg
    :target: https://pypi.python.org/pypi/SpeechRecognition/
    :alt: Development Status

.. image:: https://pypip.in/license/SpeechRecognition/badge.svg
    :target: https://pypi.python.org/pypi/SpeechRecognition/
    :alt: License

Library for performing speech recognition with the Google Speech
Recognition API.

Links:

-  `PyPI <https://pypi.python.org/pypi/SpeechRecognition/>`__
-  `GitHub <https://github.com/Uberi/speech_recognition>`__

Quickstart: ``pip install SpeechRecognition``.

Examples
--------

Recognize speech input from the microphone:

.. code:: python

                                                   # NOTE: this requires PyAudio because it uses the Microphone class
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

    try:
        print("You said " + r.recognize(audio))    # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")


Transcribe a WAV audio file:

.. code:: python

    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        print("Transcription: " + r.recognize(audio))   # recognize speech using Google Speech Recognition
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")

Transcribe a WAV audio file and show the confidence of each:

.. code:: python

    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        list = r.recognize(audio,True)                  # generate a list of possible transcriptions
        print("Possible transcriptions:")
        for prediction in list:
            print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")

Installing
----------

The easiest way to install this is using ``pip install SpeechRecognition``.

Otherwise, download the source distribution from `PyPI <https://pypi.python.org/pypi/SpeechRecognition/>`__, and extract the archive.

In the folder, run ``python setup.py install``.

Reference
---------

``Microphone(device_index = None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is available if PyAudio is available, and is undefined otherwise.

Creates a new ``Microphone`` instance, which represents a physical microphone on the computer. Subclass of ``AudioSource``.

If ``device_index`` is unspecified or ``None``, the default microphone is used as the audio source. Otherwise, ``device_index`` should be the index of the device to use for audio input.

A device index is an integer between 0 and ``pyaudio.get_device_count() - 1`` (assume we have used ``import pyaudio`` beforehand) inclusive. It represents an audio device such as a microphone or speaker. See the `PyAudio documentation <http://people.csail.mit.edu/hubert/pyaudio/docs/>`__ for more details.

This class is to be used with ``with`` statements:

.. code:: python

    with Microphone() as source:    # open the microphone and start recording
        pass                        # do things here - `source` is the Microphone instance created above
                                    # the microphone is automatically released at this point

``WavFile(filename_or_fileobject)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a new ``WavFile`` instance, which represents a WAV audio file. Subclass of ``AudioSource``.

If ``filename_or_fileobject`` is a string, then it is interpreted as a path to a WAV audio file on the filesystem. Otherwise, ``filename_or_fileobject`` should be a file-like object such as ``io.BytesIO`` or similar. In either case, the specified file is used as the audio source.

This class is to be used with ``with`` statements:

.. code:: python

    with WavFile("test.wav") as source:    # open the WAV file for reading
        pass                               # do things here - `source` is the WavFile instance created above

``Recognizer(language = "en-US", key = "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw")``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a new ``Recognizer`` instance, which represents a collection of speech recognition functionality.

The language is determined by ``language``, a standard language code, and defaults to US English.

The Google Speech Recognition API key is specified by ``key``. If not specified, it uses a generic key that works out of the box.

**WARNING: THE GENERIC KEY IS INTENDED FOR TESTING AND PERSONAL PURPOSES ONLY AND MAY BE REVOKED BY GOOGLE IN THE FUTURE.**

If you need to use this module for purposes other than these, please obtain your own API key from Google. See the "Requirements" section for more information.

``recognizer_instance.energy_threshold = 100``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the energy level threshold for sounds. Values below this threshold are considered silence. Can be changed.

This threshold is associated with the perceived loudness of the sound, but it is a nonlinear relationship. Typical values for a silent room are 0 to 1, and typical values for speaking are between 150 and 3500.

``recognizer_instance.pause_threshold = 0.8``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Represents the minimum length of silence (in seconds) that will register as the end of a phrase. Can be changed.

Smaller values result in the recognition completing more quickly, but might result in slower speakers being cut off.

``recognizer_instance.record(source, duration = None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Records up to ``duration`` seconds of audio from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.

If ``duration`` is not specified, then it will record until there is no more audio input.

``recognizer_instance.listen(source, timeout = None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Records a single phrase from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance, which it returns.

This is done by waiting until the audio has an energy above ``recognizer_instance.energy_threshold`` (the user has started speaking), and then recording until it encounters ``recognizer_instance.pause_threshold`` seconds of silence or there is no more audio input. The ending silence is not included.

The ``timeout`` parameter is the maximum number of seconds that it will wait for a phrase to start before giving up and throwing a `TimeoutException` exception. If `None`, it will wait indefinitely.

``recognizer_instance.recognize(audio_data, show_all = False)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs speech recognition, using the Google Speech Recognition API, on ``audio_data`` (an ``AudioData`` instance).

Returns the most likely transcription if ``show_all`` is ``False``, otherwise it returns a ``dict`` of all possible transcriptions and their confidence levels.

Note: confidence is set to 0 if it isn't given by Google

Also raises a ``LookupError`` exception if the speech is unintelligible, or a ``KeyError`` if the key isn't valid or the quota for the key has been maxed out.

Note: ``KeyError`` is a subclass of ``LookupError`` so a ``LookupError`` will catch both. To catch a ``KeyError`` you must place it before ``LookupError`` eg:

.. code:: python

    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        print("You said " + r.recognize(audio))         # recognize speech using Google Speech Recognition
    except KeyError:                                    # the API key didn't work
        print("Invalid API key or quota maxed out")
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")

``AudioSource``
~~~~~~~~~~~~~~~

Base class representing audio sources. Do not instantiate.

Instances of subclasses of this class, such as ``Microphone`` and ``WavFile``, can be passed to things like ``recognizer_instance.record`` and ``recognizer_instance.listen``.

``AudioData``
~~~~~~~~~~~~~

Storage class for audio data.

Contains the fields ``rate`` and ``data``, which represent the framerate and raw audio samples of the audio data, respectively.

Requirements
------------

Google Speech Recognition API requires an API key. This library defaults to using one that was reverse engineered out of Chrome, but **it is not recommended that you use this API key for anything other than personal or testing purposes**.

Instead, it is best to obtain your own API key by following the steps on the `API Keys <http://www.chromium.org/developers/how-tos/api-keys>`__ page at the Chromium Developers site.

The first software requirement is `Python 2.6, 2.7, or Python 3.3+ <https://www.python.org/download/releases/>`__. This is required to use the library.

If you want to use the ``Microphone`` class (necessary for recording from microphone input), `PyAudio <http://people.csail.mit.edu/hubert/pyaudio/#downloads>`__ is also necessary. If not installed, the library will still work, but ``Microphone`` will be undefined.

The official PyAudio builds seem to be broken on Windows. As a result, in the ``installers`` folder you will find `unofficial PyAudio builds for Windows <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio>`__ that actually work. Run the installer corresponding to your Python version to install PyAudio.

A FLAC encoder is required to encode the audio data to send to the API. If using Windows or Linux on an i385-compatible architecture, the encoder is already bundled with this library. Otherwise, ensure that you have the ``flac`` command line tool, which is often available through one's system package manager.

In summary, this library requires:

* Python 2.6, 2.7, or 3.3+
* PyAudio if you need to use microphone input.
* A FLAC encoder if not already supported.

Authors
-------

::

    Uberi <azhang9@gmail.com> (Anthony Zhang)
    bobsayshilol
    arvindch <achembarpu@gmail.com> (Arvind Chembarpu)

Please report bugs and suggestions at the `issue tracker <https://github.com/Uberi/speech_recognition/issues>`__!

License
-------

Copyright 2014 `Anthony Zhang (Uberi) <https://uberi.github.io>`__.

The source code is available online at `GitHub <https://github.com/Uberi/speech_recognition>`__.

This program is made available under the 3-clause BSD license. See ``LICENSE.txt`` for more information.
