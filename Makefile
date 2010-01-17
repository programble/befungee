# Befungee Makefile (I know it's Python, but this will be for install and clean)

all:
	@echo "I don't do anything yet. Try make hello"

hello:
	python src/befungee.py examples/helloworld.bf

beer:
	python src/befungee.py examples/catseye/beer.bf

clean:
	rm -fv *~
	cd src; $(MAKE) clean
