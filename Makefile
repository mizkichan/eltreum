dict.json: lex.csv.xz
	xz -dcvv $< | python makedict.py > $@
