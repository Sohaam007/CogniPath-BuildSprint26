CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O3
LDFLAGS = -shared

TARGET = libranker.dll
SRC = ranker.c
OBJ = $(SRC:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c ranker.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

.PHONY: all clean