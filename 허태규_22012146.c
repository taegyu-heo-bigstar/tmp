#include <stdio.h>
#include <stdlib.h>

#define SCREEN_WIDTH 4
#define MUL_M 9
#define ROW_SIZE 17
// row form "n * m = v"
// n is 1 ~ 2byte
// m is 1byte
// v is 1 ~ 3byte
// need bytes 2 + 1 + 3 + 7(space + op + \0) + 4(margin) = 17byte

static void error_print(const char *str);
static int diff(int val);
static void googoo(int start, int end, int limit);

//user define functions and structure
typedef struct n_dan
{
	int num;
	char *row[MUL_M];
} n_dan;
typedef struct n_dans
{
	n_dan dan_p[SCREEN_WIDTH];
	int len;
} n_dans;
static char * generate_row(int num, int mul_num);	//곱해진 행을 출력하는 함수
static void init_n_dan(n_dan * const dan, int num);	//num을 기준으로 n 단의 텍스트를 생성, 저장하는 함수
static void init_n_dans(n_dans * const dans, int start, int len);	//매개변수로 주어진 값으로 단들을 초기화하는 함수
static void print_n_dans(const n_dans * dans);	//단들에 저장된 정보를 출력
static void	row_add(char *row, const char *src, int width);	//generate_row의 helper function

//42school's functions
char * ft_itoa(int num);
size_t ft_strlen(const char *str);
size_t	ft_strlcat(char *dst, const char *src, size_t size);

int main(int argc, char *argv[])
{
	int i, ch, temp[3];

	if (argc != 4)
	{
		printf("사용법 : %s [시작 단] [끝 단] [출력라인수]\n", argv[0]);
		printf("주의 : - 시작, 끝 단, 출력라인수는 1~99까지의 숫자만 넣으세요\n");
		printf(" - 시작 단이 끝 단 보다 크면 안됩니다\n");
		printf("예) %s 3 90 4\n", argv[0]);
		exit(1);
	}

	for (i = 1; i < 3; i++) //시작, 끝단의 제한
	{
		ch = atoi(argv[i]);
		temp[i] = ch;
		if (diff(ch) == 0)
			error_print("1 ~ 99까지의 숫자만 넣으세요");
	}

	if (temp[1] > temp[2]) //시작 단이 끝 단 보다 크지 않도록 제한
		error_print("시작 단이 끝 단 보다 크면 안됩니다");

	temp[0] = atoi(argv[3]);
	if (diff(temp[0]) == 0) //컬럼의 제한
		error_print("1~99까지의 숫자만 넣으세요");

	googoo(temp[1], temp[2], temp[0]); //구구단

	return 0;
}

static void error_print(const char *str)
{
	printf("%s\n", str);
	exit(1);
}

static int diff(int num)
{
	if (num < 1 || 99 < num)
		return 0;
	else
		return 1;
}

static void googoo(int start, int end, int limit)
{
	int current_print_dans_len;	//현재 출력할 단들의 길이
	int left;	//limit에서 current_print_dans_len을 제외한 값
	n_dans dans;

	end++;
	while(start < end)
	{
		
		left = end - start < limit ? end - start : limit;	//left는 이번 루프에서 출력해야할 논리적 길이 단위(최대길이 limit) 
		while (left)
		{
			current_print_dans_len = left < SCREEN_WIDTH ? left : SCREEN_WIDTH;
			init_n_dans(&dans, start, current_print_dans_len);
			print_n_dans(&dans);
			start += current_print_dans_len;
			left -= current_print_dans_len;
		}
	}
}

static void init_n_dan(n_dan * const dan, int num)
{
	if (dan == NULL || num < 1)
		return ;
	for (int i = 1; i <= MUL_M; i++)
	{
		dan->row[i - 1] = generate_row(num, i);
	}
}

static void init_n_dans(n_dans * const dans, int start, int len)
{
	if (dans == NULL || len < 1)
		return ;
	dans->len = len;
	for (int i = 0; i < dans->len; i++)
	{
		init_n_dan(&dans->dan_p[i], start + i);
	}
}

static void print_n_dans(const n_dans *dans)
{
	int	row;
	int	col;

	if (dans == NULL)
		return ;
	row = 0;
	while (row < MUL_M)
	{
		col = 0;
		while (col < dans->len)
		{
			if (dans->dan_p[col].row[row] != NULL)
				printf("%s", dans->dan_p[col].row[row]);
			col++;
		}
		printf("\n");
		row++;
	}
	printf("\n");
}

static char	*generate_row(int num, int mul_num)
{
	char	*row;
	char	*num_str;
	char	*mul_str;
	char	*val_str;

	row = (char *)malloc(sizeof(char) * ROW_SIZE);
	num_str = ft_itoa(num);
	mul_str = ft_itoa(mul_num);
	val_str = ft_itoa(num * mul_num);
	if (!row || !num_str || !mul_str || !val_str)
		error_print("generate failed");
	row[0] = '\0';
	row_add(row, num_str, 2);
	row_add(row, " * ", 0);
	row_add(row, mul_str, 0);
	row_add(row, " = ", 0);
	row_add(row, val_str, 3);
	row_add(row, "    ", 0);
	return (row);
}

static void	row_add(char *row, const char *src, int width)
{
	int	pad;

	pad = width - (int)ft_strlen(src);
	while (pad > 0)
	{
		ft_strlcat(row, " ", ROW_SIZE);
		pad--;
	}
	ft_strlcat(row, src, ROW_SIZE);
}

//42school's functions definitions
static int	get_len(long n)
{
	int	len;

	len = 0;
	if (n <= 0)
		len++;
	while (n != 0)
	{
		n /= 10;
		len++;
	}
	return (len);
}

char	*ft_itoa(int n)
{
	char	*str;
	int		len;
	long	nbr;

	nbr = n;
	len = get_len(nbr);
	str = (char *)malloc(sizeof(char) * (len + 1));
	if (!str)
		return (NULL);
	str[len] = '\0';
	if (nbr == 0)
		str[0] = '0';
	if (nbr < 0)
	{
		str[0] = '-';
		nbr = -nbr;
	}
	while (nbr > 0)
	{
		str[--len] = (nbr % 10) + '0';
		nbr /= 10;
	}
	return (str);
}

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	dst_len;
	size_t	src_len;
	size_t	i;

	dst_len = ft_strlen(dst);
	src_len = ft_strlen(src);
	if (size <= dst_len)
		return (size + src_len);
	i = 0;
	while (src[i] && (dst_len + i + 1) < size)
	{
		dst[dst_len + i] = src[i];
		i++;
	}
	dst[dst_len + i] = '\0';
	return (dst_len + src_len);
}

size_t	ft_strlen(const char *s)
{
	size_t	len;

	len = 0;
	while (s && s[len])
		len++;
	return (len);
}