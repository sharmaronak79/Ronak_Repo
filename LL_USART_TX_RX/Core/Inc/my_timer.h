/*
 * my_timer.h
 *
 *  Created on: May 30, 2024
 *      Author: ronak
 */

#ifndef INC_MY_TIMER_H_
#define INC_MY_TIMER_H_

#include "stm32l4xx_ll_tim.h"
#include "stm32l4xx_ll_bus.h"
#include "stm32l4xx_ll_rcc.h"

// Function prototypes
void MY_TIMER_Init(void);
void MY_Delay(uint32_t ms);

#endif /* INC_MY_TIMER_H_ */
