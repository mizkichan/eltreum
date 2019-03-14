dict.json: lex.csv
	python3 makedict.py < $< > $@
