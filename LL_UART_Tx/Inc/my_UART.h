/*
 * my_UART.h
 *
 *  Created on: May 24, 2024
 *      Author: Ronakkumar_Sharma
 */

#ifndef MY_UART_H_
#define MY_UART_H_

#include "stm32l496xx.h"
#include "stm32l4xx_ll_bus.h"
#include "stm32l4xx_ll_usart.h"
#include "stm32l4xx_ll_gpio.h"

void usart1_init(void);
void usart1_write(int ch);


#endif /* MY_UART_H_ */
