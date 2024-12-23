/*
 * my_UART.c
 *
 *  Created on: May 27, 2024
 *      Author: ronak
 */

#include "my_uart.h"
#include "my_timer.h"

//void uart_write(USART_TypeDef* ,uint8_t ch){
//	while(! LL_USART_IsActiveFlag_TXE(USART1)){
//
//		  	}
//		  LL_USART_TransmitData8(USART1, ch);
//}

//void uart_write(USART_TypeDef *huart ,const uint8_t *pdata, uint16_t size){
//	while(size>0){
//		while(! LL_USART_IsActiveFlag_TXE(USART1)){
//
//		  	}
//		LL_USART_TransmitData8(USART1, ( uint8_t )pdata);
//		pdata++;
//		size--;
//	}
//}


void uart_write(USART_TypeDef *huart,const char *data) {
    while (*data) {
        // Wait until the data register is empty
        while (!LL_USART_IsActiveFlag_TXE(USART1));

        // Transmit the character
        LL_USART_TransmitData8(USART1, *data++);

        // Wait until the transmission is complete
        while (!LL_USART_IsActiveFlag_TC(USART1));
    }
    MY_Delay(500);

}
