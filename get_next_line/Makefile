NAME = get_next_line

CC = cc
CFLAGS = -Wall -Wextra -Werror

ifdef BUFFER_SIZE
CFLAGS += -D BUFFER_SIZE=$(BUFFER_SIZE)
endif

ifdef BONUS_FLAG
	SRC_FILES = get_next_line_bonus.c get_next_line_utils_bonus.c
	HEADER = get_next_line_bonus.h
	TEST_NAME = bonus
else
	SRC_FILES = get_next_line.c get_next_line_utils.c
	HEADER = get_next_line.h
	TEST_NAME = basic
endif

SRC = $(SRC_FILES) main.c
OBJ = $(SRC:.c=.o)

ifdef STDIN
FD_NAME = /dev/stdin
endif

ifndef FD_NAME
FD_NAME = test.txt
endif

test: $(NAME) $(FD_NAME) clean test.txt
	@echo "\n$(NAME)'s $(TEST_NAME) test"
	@echo "********************"
	@./$(NAME)
	@echo "********************"
	@echo ""

all: test

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) -o $(NAME) $(OBJ)

main.c:
ifdef BONUS_FLAG
	@echo '#include <fcntl.h>' > main.c
	@echo '#include <stdio.h>' >> main.c
	@echo '#include "$(HEADER)"' >> main.c
	@echo '' >> main.c
	@echo 'int main(void)' >> main.c
	@echo '{' >> main.c
	@echo '	int		fd1, fd2, fd3;' >> main.c
	@echo '	char	*line;' >> main.c
	@echo '' >> main.c
	@echo '	fd1 = open("test1.txt", O_RDONLY);' >> main.c
	@echo '	fd2 = open("test2.txt", O_RDONLY);' >> main.c
	@echo '	fd3 = open("test3.txt", O_RDONLY);' >> main.c
	@echo '	if (fd1 == -1 || fd2 == -1 || fd3 == -1)' >> main.c
	@echo '	{' >> main.c
	@echo '		perror("Error opening file");' >> main.c
	@echo '		return (1);' >> main.c
	@echo '	}' >> main.c
	@echo '	line = get_next_line(fd1); if (line) { printf("fd1: %s", line); free(line); }' >> main.c
	@echo '	line = get_next_line(fd2); if (line) { printf("fd2: %s", line); free(line); }' >> main.c
	@echo '	line = get_next_line(fd3); if (line) { printf("fd3: %s", line); free(line); }' >> main.c
	@echo '	line = get_next_line(fd1); if (line) { printf("fd1: %s", line); free(line); }' >> main.c
	@echo '	line = get_next_line(fd2); if (line) { printf("fd2: %s", line); free(line); }' >> main.c
	@echo '	close(fd1); close(fd2); close(fd3);' >> main.c
	@echo '	return (0);' >> main.c
	@echo '}' >> main.c
else
	@echo '#include <fcntl.h>' > main.c
	@echo '#include <stdio.h>' >> main.c
	@echo '#include "$(HEADER)"' >> main.c
	@echo '' >> main.c
	@echo 'int main(void)' >> main.c
	@echo '{' >> main.c
	@echo '	int		fd;' >> main.c
	@echo '	char	*line;' >> main.c
	@echo '' >> main.c
	@echo '	fd = open("$(FD_NAME)", O_RDONLY);' >> main.c
	@echo '	if (fd == -1)' >> main.c
	@echo '	{' >> main.c
	@echo '		perror("Error opening file");' >> main.c
	@echo '		return (1);' >> main.c
	@echo '	}' >> main.c
	@echo '	while ((line = get_next_line(fd)) != NULL)' >> main.c
	@echo '	{' >> main.c
	@echo '		printf("%s", line);' >> main.c
	@echo '		free(line);' >> main.c
	@echo '	}' >> main.c
	@echo '	close(fd);' >> main.c
	@echo '	return (0);' >> main.c
	@echo '}' >> main.c
endif

test.txt:
ifdef BONUS_FLAG
	@echo 'File 1 Line 1' > test1.txt
	@echo 'File 1 Line 2' >> test1.txt
	@echo 'File 2 Line 1' > test2.txt
	@echo 'File 2 Line 2' >> test2.txt
	@echo 'File 3 Line 1' > test3.txt
	@echo 'File 3 Line 2' >> test3.txt
else
	@echo 'Hello World' > test.txt
	@echo 'This is a test' >> test.txt
	@echo '42 Seoul' >> test.txt
	@echo 'Get Next Line' >> test.txt
	@echo 'End of file' >> test.txt
endif

bonus: fclean
	@$(MAKE) BONUS_FLAG=1

clean:
	rm -f main.c *.o

fclean: clean
	rm -f $(NAME) $(FD_NAME) test1.txt test2.txt test3.txt

re: fclean all

reBonus: fclean all bonus

%.o: %.c $(HEADER)
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: all bonus clean fclean re reBonus test
