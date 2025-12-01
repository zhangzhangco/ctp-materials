# Makefile for CTP Tools

CC = cc
CXX = c++
CFLAGS = -Wall -O2
CXXFLAGS = -Wall -O2

# Libraries
LIBS_CRYPTO = -lcrypto
LIBS_XERCES = -lxerces-c
LIBS_OPENJPEG = -lopenjpeg
LIBS_KDM = -lxerces-c -lxml-security-c -lkumu -lcrypto

# Targets
TARGETS = dc-thumbprint schema-check j2c-scan kdm-decrypt

all: $(TARGETS)

dc-thumbprint: dc-thumbprint.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS_CRYPTO)

schema-check: schema-check.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LIBS_XERCES)

j2c-scan: j2c-scan.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LIBS_OPENJPEG)

kdm-decrypt: kdm-decrypt.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LIBS_KDM)

clean:
	rm -f $(TARGETS)

.PHONY: all clean
