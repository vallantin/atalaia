
# Atalaia - Text Preprocessing NLP

*  [Lima Vallantin](https://vallant.in/)
  
Atalaia is a collection of methods that can be used for simple Text Preprocessing tasks. It can be used for tasks involving text preprocessing for machine learning. Atalaia works mainly with text strings and lists of strings.  

The library is developed in Python 3.

## Installing Atalaia

### locally (last version)

    $ python setup.py install

## Installing the requirements

	$ pip install -r requirements.txt

If you want, you can also install Atalaia in a virtual environment:

	$ python -m venv .env

	$ source .env/bin/activate

	$ pip3 install atalaia
  
### Prerequisites

Atalaia uses external Python libraries. They are all documented in the [requirements.txt](requirements.txt) file.

## Usage examples

To use Atalaia, initialize it by choosing one of the three available languages ('en', 'fr', 'pt-br')

	from atalaia.atalaia import Atalaia
	atalaia_en = Atalaia('en')

### Quick preprocessing

Atalaia has the preprocess method, which applies commonly used preprocessed steps on you text.

	text = "At the end of the day, you're solely responsible for your success and your failure. And the sooner you realize that, you accept that, and integrate that into your work ethic, you will start being successful. As long as you blame others for the reason you aren't where you want to be, you will always be a failure."
	preprocessed_text = atalaia_en.preprocess(text)
	print(preprocessed_text)
	
	>>> ['at', 'the', 'end', 'of', 'the', 'day', 'you', 'are', 'sole', 'respons', 'for', 'your', 'success', 'and', 'your', 'failur', 'and', 'the', 'sooner', 'you', 'realiz', 'that', 'you', 'accept', 'that', 'and', 'integr', 'that', 'into', 'your', 'work', 'ethic', 'you', 'will', 'start', 'be', 'success', 'as', 'long', 'as', 'you', 'blame', 'other', 'for', 'the', 'reason', 'you', 'are', 'not', 'where', 'you', 'want', 'to', 'be', 'you', 'will', 'alway', 'be', 'a', 'failur']

If you prefer, you can choose to:

- tokenize the sentence

- stem it

- remove stop words

- pos tag the portuguese sentences

		text = "At the end of the day, you're solely responsible for your success and your failure. And the sooner you realize that, you accept that, and integrate that into your work ethic, you will start being successful. As long as you blame others for the reason you aren't where you want to be, you will always be a failure."

		preprocessed_text = atalaia_en.preprocess(text, stem=False, remove_stopwords=True)

		print(preprocessed_text)

		['end', 'day', 'solely', 'responsible', 'success', 'failure', 'sooner', 'realize', 'that', 'accept', 'that', 'integrate', 'work', 'ethic', 'start', 'successful', 'long', 'blame', 'others', 'reason', 'want', 'be', 'always', 'failure']

### List preprocessing

If you have a list of sentences or you are using Pandas, you can pass the entire list for preprocessing by using the preprocess_list method.

	list_of_strings = ['I love you',
						'Please, never leave me alone',
						'If you go, I will die',
						'I am watching a lot of romantic comedy lately',
						'I have to eat icecream' ]

	list_processed = atalaia_en.preprocess_list(list_of_strings, stem=False, remove_stopwords=True)

	print(list_processed)

	>>> [['love'], ['please', 'never', 'leave', 'alone'], ['go', 'die'], ['watching', 'lot', 'romantic', 'comedy', 'lately'], ['eat', 'icecream']]

### Defining your own pipeline

Use the single available methods to create a custom pipeline instead of using the quick preprocessing function.

	text = "At the end of the day, @john you're solely responsible for your #success and your #failure. And the sooner you realize that, you accept that, and integrate that into your work ethic, you will start being #successful."
	text = atalaia_en.lower_remove_white(text)
	text = atalaia_en.expand_contractions(text)
	text = atalaia_en.replace_handles(text, 'HANDLE')
	text = atalaia_en.replace_hashtags(text, 'HASHTAG')
	text = atalaia_en.remove_stopwords(text)
	text = atalaia_en.replace_punctuation(text, placeholder='PUNCTUATION')
	text = atalaia_en.tokenize(text)
	print(text)

	>>> ['end', 'day', 'PUNCTUATION', 'HANDLE', 'solely', 'responsible', 'HASHTAG', 'HASHTAG', 'PUNCTUATION', 'sooner', 'realize', 'that', 'PUNCTUATION', 'accept', 'that', 'PUNCTUATION', 'integrate', 'work', 'ethic', 'PUNCTUATION', 'start', 'HASHTAG', 'PUNCTUATION']

## Development

### Testing

1. Create a clean test environment

2. Navigate to atalaia project on your computer and generate a package using bdist_wheel

		$ python3 setup.py sdist bdist_wheel

3. Install the package
					
		$ python3 setup.py install

### Docs

Navigate to atalaia/atalaia and type:

	$ pdoc --html atalaia

### Release

Follow the steps below before releasing a new version:

1. Update all necessary documents

2. Generate the package using bdist

	python setup.py bdist_rpm

3. Install the new version on a clean environment for testing

4. If everything is ok, generate the doc using pdoc

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Use [SemVer](http://semver.org/) for versioning.

## Authors

*  **Lima Vallantin** - *Initial work* - [Lima Vallantin](https://vallant.in/)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details

# V 0.0.1
##  New features
- 
# Improvements
- 