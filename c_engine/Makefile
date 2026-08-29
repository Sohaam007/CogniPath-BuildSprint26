CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O3 -fopenmp
LDFLAGS = -shared -fopenmp

ifeq ($(OS),Windows_NT)
    TARGET = libranker.dll
else
    TARGET = libranker.so
endif

SRC = ranker.c
OBJ = $(SRC:.c=.o)

all: $(TARGET) ranker.so

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

ranker.so: $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c ranker.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET) libranker.dll ranker.so

.PHONY: all clean
