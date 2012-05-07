# Python Semantic Natural Language Processing for Human Robot Interaction

This is a python script to interact with Stanford University's NLP group's Java-based [CoreNLP tools](http://nlp.stanford.edu/softwar/corenlp.shtml). It will provide a simple output for the easy parsing of basic imperative sentences to machine usable forms including basic direct objects and preposional phrases. The actual code to parse and output the machine code is around 50 total lines (not including helpers) and can easily be updated or modified to include any sentence types and structures you need. 

This project was part of a project and was created after finding paper after paper about NLP use in HRI but no simple, extensible, platform agnostic code.

This was based on a project by Dustin Smith's python wrapper for the [CoreNLP tools](http://nlp.stanford.edu/softwar/corenlp.shtml) his documentation for the server is below followed by my instructions to obtain a default parse:

# Python interface to Stanford Core NLP tools v1.3.1

This is a Python wrapper for Stanford University's NLP group's Java-based [CoreNLP tools](http://nlp.stanford.edu/software/corenlp.shtml).  It can either be imported as a module or run as a JSON-RPC server. Because it uses many large trained models (requiring 3GB RAM on 64-bit machines and usually a few minutes loading time), most applications will probably want to run it as a server.


   * Python interface to Stanford CoreNLP tools: tagging, phrase-structure parsing, dependency parsing, named entity resolution, and coreference resolution.
   * Runs an JSON-RPC server that wraps the Java server and outputs JSON.
   * Outputs parse trees which can be used by [nltk](http://nltk.googlecode.com/svn/trunk/doc/howto/tree.html).
   * Output can be interpreted by `parse.py` and will output machine and human readable commands for simple HRI.


It requires [pexpect](http://www.noah.org/wiki/pexpect) and (optionally) [unidecode](http://pypi.python.org/pypi/Unidecode) to handle non-ASCII text.  This script includes and uses code from [jsonrpc](http://www.simple-is-better.org/rpc/) and [python-progressbar](http://code.google.com/p/python-progressbar/).

It runs the Stanford CoreNLP jar in a separate process, communicates with the java process using its command-line interface, and makes assumptions about the output of the parser in order to parse it into a Python dict object and transfer it using JSON.  The parser will break if the output changes significantly, but it has been tested on **Core NLP tools version 1.3.1** released 2012-04-09.

## Download and Usage 

To use this program you must [download](http://nlp.stanford.edu/software/corenlp.shtml#Download) and unpack the tgz file containing Stanford's CoreNLP package.  By default, `corenlp.py` looks for the Stanford Core NLP folder as a subdirectory of where the script is being run.

In other words: 

    sudo pip install pexpect unidecode   # unidecode is optional
	git clone git://github.com/dasmith/stanford-corenlp-python.git
	cd stanford-corenlp-python
    wget http://nlp.stanford.edu/software/stanford-corenlp-2012-04-09.tgz
    tar xvfz stanford-corenlp-2012-04-09.tgz

Then, to launch a server:

    python corenlp.py

Optionally, you can specify a host or port:

    python corenlp.py -H 0.0.0.0 -p 3456

That will run a public JSON-RPC server on port 3456.

Assuming you are running on port 8080, the code in `parse.py` shows an example parse: 

    python parse.py "Pick up the biggest red ball to the left of the green square."

This will print out a list of regular commands for the robot:

    Filter square
    Filter green
    remember
    Filter left
    Filter ball
    Filter red
    Filter biggest
    pick

This output can be easily modified to suit your robotic system and the dictionary is stored in the file `dict.json` for easy access, simply add synonyms and lemmas you are interested in. Any word in that file will be replaced in the json object returned (including preposition typed dependencies (i.e. `prep_on( gov, dep)` to `prep_to( gov, dep)`)


## Questions 

**Stanford CoreNLP tools require a large amount of free memory**.  While this program uses only a subset of the features available (you can enable more in `corenlp.py`, it is still a memory hog, especially on embeded systems. Java 5+ uses about 50% more RAM on 64-bit machines than 32-bit machines.  32-bit machine users can lower the memory requirements by changing `-Xmx3g` to `-Xmx2g` or even less.
If pexpect timesout while loading models, check to make sure you have enough memory and can run the server alone without your kernel killing the java process:

    java -cp stanford-corenlp-2011-09-16.jar:stanford-corenlp-2011-09-14-models.jar:xom.jar:joda-time.jar -Xmx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -props default.properties

You can reach me, Chase, by sending a message on GitHub.

# Contributors

This is free and open source software and has benefited from the contribution and feedback of others.  Like Stanford's CoreNLP tools, it is covered under the [GNU General Public License v2 +](http://www.gnu.org/licenses/gpl-2.0.html), which in short means that modifications to this program must maintain the same free and open source distribution policy.

  * Dustin Smith dasmith
  * Justin Cheng jcccf@221513ecf322dc32d6e088fb2f68751e45bac226
  * Abhaya Agarwal 8ed7640388cac8ba6d897739f5c8fe24eb87cc48

