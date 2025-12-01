# Makefile for CTP Tools

CC = cc
CXX = c++
CFLAGS += -Wall -O2
CXXFLAGS += -Wall -O2

# Libraries
LIBS_CRYPTO = -lcrypto
LIBS_XERCES = -lxerces-c
LIBS_OPENJPEG = -lopenjpeg
LIBS_KDM = -lxerces-c -lxml-security-c -lkumu -lcrypto

# Targets
TARGETS = dc-thumbprint schema-check j2c-scan kdm-decrypt

all: $(TARGETS)

dc-thumbprint: dc-thumbprint.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $< $(LIBS_CRYPTO)

schema-check: schema-check.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $< $(LIBS_XERCES)

j2c-scan: j2c-scan.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $(shell pkg-config --cflags libopenjp2) -o $@ $< $(LIBS_OPENJPEG) $(shell pkg-config --libs libopenjp2)

kdm-decrypt: kdm-decrypt.cpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $< $(LIBS_KDM)

clean:
	rm -f $(TARGETS)

.PHONY: all clean
