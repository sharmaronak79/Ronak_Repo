/*
 * my_uart.h
 *
 *  Created on: May 27, 2024
 *      Author: ronak
 */

#ifndef INC_MY_UART_H_
#define INC_MY_UART_H_

#include <stdint.h>
#include "main.h"
#define RX_BUF_SIZE		256


 /* *********************************************************
 * Typedefs
 * ***********************************************************/

typedef struct{
	USART_TypeDef *handle;
	uint8_t rx_buf[RX_BUF_SIZE];
}usart_handle_t;

/* *********************************************************
 * Global variable Declarations
 * ***********************************************************/

extern usart_handle_t usart_dev;


void uart_write(USART_TypeDef *huart,const char *pdata);

#endif /* INC_MY_UART_H_ */
