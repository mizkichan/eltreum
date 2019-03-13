%.csv: lex.csv.xz
	xz -dcvv $< | ./dictfilter.py > $@
