/*
 * my_UART.c
 *
 *  Created on: May 24, 2024
 *      Author: Ronakkumar_Sharma
 */
#include<stdio.h>
#include "my_UART.h"


void usart1_init(){

	// Here we are using GPIOB , PB6->Tx and PB7->Rx
	/*1. Enable clock access for USART GPIO Pins*/
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOB);

	/*2. Enable clock access for USART module*/
	LL_APB2_GRP1_EnableClock (LL_APB2_GRP1_PERIPH_USART1);

	/*3. Set mode of USART Tx pin to alternate function */
	LL_GPIO_SetPinMode (GPIOB,LL_GPIO_PIN_6 , LL_GPIO_MODE_ALTERNATE);

	/*4. Select USART Tx alternate function type*/
	LL_GPIO_SetAFPin_0_7 (GPIOB, LL_GPIO_PIN_6,LL_GPIO_AF_7 );

	/*5. Configure USART protocol parameters*/
	LL_USART_Disable(USART1);
	LL_USART_SetTransferDirection (USART1,LL_USART_DIRECTION_TX );

	LL_USART_ConfigCharacter (USART1, LL_USART_DATAWIDTH_8B,LL_USART_PARITY_NONE, LL_USART_STOPBITS_1);

	LL_USART_SetBaudRate (USART1,16000000, LL_USART_OVERSAMPLING_16,115200);


	LL_USART_Enable (USART1);
	LL_USART_EnableDirectionTx (USART1);

}
void usart1_write(int ch){

	/* Wait for TXE flag to be raised*/
	while(! LL_USART_IsActiveFlag_TXE(USART1)){
		LL_USART_TransmitData8(USART1, ch);
	}



}
