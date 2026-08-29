CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O3
LDFLAGS = -shared

ifeq ($(OS),Windows_NT)
    TARGET = libranker.dll
else
    TARGET = libranker.so
endif

SRC = ranker.c
OBJ = $(SRC:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c ranker.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET) libranker.dll libranker.so

.PHONY: all clean
