dict.json: lex.csv.xz
	xz -dcvv $< | python3 makedict.py > $@
