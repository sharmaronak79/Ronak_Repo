/*
 * USART1.c
 *
 *  Created on: Jun 20, 2024
 *      Author: Ronakkumar_Sharma
 */

#include "main.h"


void uart1_init(void){

	/*1. Enable the clock access for UART1 GPIO Pin*/
			//PA9 -> Tx
			//PA10 -> Rx, So, Enable clock for port A
	LL_AHB2_GRP1_EnableClock(LL_AHB2_GRP1_PERIPH_GPIOA);

	/*2. Enable the clock access for UART1 GPIO module*/
	LL_APB2_GRP1_EnableClock(LL_APB2_GRP1_PERIPH_USART1);

	/*3. Set mode of UART Tx and Rx pin to alternate function*/
	LL_GPIO_SetPinMode(GPIOA, LL_GPIO_PIN_9 , LL_GPIO_MODE_ALTERNATE);
	LL_GPIO_SetPinMode(GPIOA, LL_GPIO_PIN_10, LL_GPIO_MODE_ALTERNATE);

	/*4. Select UART Tx and Rx alternate function type*/
	LL_GPIO_SetAFPin_8_15(GPIOA, LL_GPIO_PIN_9, LL_GPIO_AF_7);
	LL_GPIO_SetAFPin_8_15(GPIOA, LL_GPIO_PIN_10, LL_GPIO_AF_7);


	/*5. Configure UART protocol parameter*/
	LL_USART_Disable(USART1);
	LL_USART_SetTransferDirection(USART1, LL_USART_DIRECTION_TX_RX);
	LL_USART_ConfigCharacter(USART1	, LL_USART_DATAWIDTH_8B, LL_USART_PARITY_NONE, LL_USART_STOPBITS_1);
	LL_USART_SetBaudRate(USART1,16000000 , LL_USART_OVERSAMPLING_16, 115200); //Need to chanage clock
	LL_USART_Enable(USART1);

}

void uart1_write(int ch){

	/*Wait for the TXE flag to be set*/
	while(! LL_USART_IsActiveFlag_TXE(USART1)){};
	LL_USART_TransmitData8(USART1, ch);

}

char uart1_read(void){
	/*Wait for RXNE flag to be set*/
	while(! LL_USART_IsActiveFlag_RXNE(USART1)){};
	return LL_USART_ReceiveData8(USART1);

}
















