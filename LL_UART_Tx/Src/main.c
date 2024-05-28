#include "my_UART.h"

int main(){

	usart1_init();

	while(1){
		usart1_write('Y');
		for(int itr = 0;itr < 90000;itr++){};
	}


	return 0;
}
