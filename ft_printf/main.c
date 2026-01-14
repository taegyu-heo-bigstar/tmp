#include "ft_printf.h"
#include <stdio.h>

#define FUNC_NAME(f) #f

void test_function(int (*fp)(const char *, ...), char *func_name)
{
	printf("This is a test for %s:\n\n", func_name);

	printf("----------TEST %s-----------\n", func_name);
	int len1 = fp("Character: %c\n", 'A');
	printf("Length returned by %s: %d\n\n", func_name, len1);

	int len2 = fp("String: %s\n", "Hello, World!");
	printf("Length returned by %s: %d\n\n", func_name, len2);

	int len3 = fp("Integer: %d\n", 42);
	printf("Length returned by %s: %d\n\n", func_name, len3);

	int len4 = fp("Unsigned Integer: %u\n", 42);
	printf("Length returned by %s: %d\n\n", func_name, len4);

	int len5 = fp("Hexadecimal (lowercase): %x\n", 255);
	printf("Length returned by %s: %d\n\n", func_name, len5);

	int len6 = fp("Hexadecimal (uppercase): %X\n", 255);
	printf("Length returned by %s: %d\n\n", func_name, len6);

	int len7 = fp("Pointer: %p\n", (void *)0x12345678);
	printf("Length returned by %s: %d\n\n", func_name, len7);

	int len8 = fp("Percent sign: %%\n");
	printf("Length returned by %s: %d\n", func_name, len8);
	printf("-----------------------------------\n");
}

int main(void)
{
	test_function(&printf, FUNC_NAME(printf));	//printf test
	printf("\n");

	test_function(&ft_printf, FUNC_NAME(ft_printf)); //ft_printf test
	printf("\n");


	char str = (char *)malloc(65536 * sizeof(char));
	if (!str)
		return (1);
	int mode;
	int len;
	while (1)	//interactive test
	{
		int mode;
		printf("select mode (1: printf, 2: ft_printf, other: exit): ");
		scanf("%d", &mode);
		if (mode != 1 && mode != 2)
			break ;
		printf("Enter a string to print: ");
		scanf("%s", str);
		if (mode == 1)
			printf("%s\n", str);
		else if(mode == 2)
			ft_printf("%s\n", str);
		else
			break ;
	}
	free(str);

	return (0);
}
