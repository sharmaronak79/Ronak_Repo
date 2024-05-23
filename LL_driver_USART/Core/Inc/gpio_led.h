/*
 * gpio_led.h
 *
 *  Created on: May 22, 2024
 *      Author: ronak
 */

#ifndef INC_GPIO_LED_H_
#define INC_GPIO_LED_H_

#include "stm32l4xx_ll_bus.h"
#include "stm32l4xx_ll_gpio.h"

void button_led(void);
void btn_seq_led(void);

#endif /* INC_GPIO_LED_H_ */
