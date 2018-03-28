.PHONY: zip

zip:
	rm -f zip/geo.py
	cd geo; zip -r ../zip/geo *
	mv zip/geo.zip zip/geo.py
