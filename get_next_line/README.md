makefile 사용법 안내

1. make (test) : 필수 과제가 컴파일됨
2. make STDIN=1 : 필수 과제에서 읽어들이는 파일 디스크립터를 표준 입력으로 함.
3. make bonus : bonus 과제가 컴파일됨
4. make clean : 테스팅에 불필요한 목적 파일과 메인 함수 코드를 삭제
5. make fclean : 테스팅에 필요한 실행 파일과 텍스트 파일도 삭제
6. make BUFFER_SIZE=42 : read 함수가 사용할 버퍼의 크기를 42바이트로 설정
7. make FD_NAME=test.txt : 필수 과제에 사용할 테스팅 파일의 이름을 test.txt 파일로 설정
8. make re : 필수 과제를 다시 컴파일
9. make reBonus : bonus 과제를 다시 컴파일
10. make all : maek test와 동일
