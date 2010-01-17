# Befungee Makefile (I know it's Python, but this will be for install and clean)

all:
	@echo "I don't do anything yet. Try make clean."

clean:
	rm -fv *~
	cd src; $(MAKE) clean
