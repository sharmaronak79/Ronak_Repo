/*
 * my_timer.c
 *
 *  Created on: May 30, 2024
 *      Author: ronak
 */


#include "my_timer.h"

void MY_TIMER_Init(void) {
    // Enable the clock for TIM2
    LL_APB1_GRP1_EnableClock(LL_APB1_GRP1_PERIPH_TIM2);

    // Set the TIM2 prescaler to have the counter clocked at 1 MHz (assuming the system clock is 80 MHz)
    LL_TIM_SetPrescaler(TIM2, __LL_TIM_CALC_PSC(SystemCoreClock, 1000000));

    // Set the auto-reload value to have the counter overflow at 1 kHz
    LL_TIM_SetAutoReload(TIM2, __LL_TIM_CALC_ARR(SystemCoreClock/2, LL_TIM_GetPrescaler(TIM2), 1000));

    // Enable the update interrupt
    LL_TIM_EnableIT_UPDATE(TIM2);

    // Enable the counter
    LL_TIM_EnableCounter(TIM2);

    // Wait for the update event to make sure the timer is properly initialized
    while(!LL_TIM_IsActiveFlag_UPDATE(TIM2));

    // Clear the update flag
    LL_TIM_ClearFlag_UPDATE(TIM2);
}

void MY_Delay(uint32_t ms) {
    uint32_t start_time = LL_TIM_GetCounter(TIM2);
    while ((LL_TIM_GetCounter(TIM2) - start_time) < ms);
}
