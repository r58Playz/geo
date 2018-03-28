.PHONY: zip

zip:
	rm -f zip/geo.zip
	cd geo; zip -r ../zip/geo *
