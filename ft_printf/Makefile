CC = gcc
CFLAGS = -Wall -Wextra -Werror
TARGET = test_app
SRCS = test.c
OBJS = $(SRCS:.c=.o)
LIBS = -L. -lftprintf

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -fsanitize=address -g -no-pie $(OBJS) $(LIBS) -o $(TARGET)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(TARGET)

re: fclean all

.PHONY: all clean fclean re
