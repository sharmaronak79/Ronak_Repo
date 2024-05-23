/*
 * gpio_led.c
 *
 *  Created on: May 22, 2024
 *      Author: ronak
 */

#include "gpio_led.h"

void button_led(){
/* Enable clock for a GPIOB and GPIOC */
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOB);
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOC);

	/* set a pin and output type*/
	LL_GPIO_SetPinMode (GPIOB,LL_GPIO_PIN_7 , LL_GPIO_MODE_OUTPUT);
	LL_GPIO_SetPinMode (GPIOB,LL_GPIO_PIN_14 , LL_GPIO_MODE_OUTPUT);
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_7 , LL_GPIO_MODE_OUTPUT);

	/* Set PC13 as inout user button*/
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_13 , LL_GPIO_MODE_INPUT);

	while(1)
	{
		if (LL_GPIO_IsInputPinSet (GPIOC,LL_GPIO_PIN_13 ))
		{

			LL_GPIO_SetOutputPin (GPIOB,LL_GPIO_PIN_7 | LL_GPIO_PIN_14 );
			LL_GPIO_SetOutputPin (GPIOC,LL_GPIO_PIN_7 );
		}else
		{
			LL_GPIO_ResetOutputPin (GPIOB,LL_GPIO_PIN_7 | LL_GPIO_PIN_14);
			LL_GPIO_ResetOutputPin (GPIOC,LL_GPIO_PIN_7 );
		}
	}
}

void btn_seq_led(void){
	/* Enable clock for a GPIOB and GPIOC */
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOB);
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOC);

	/* set a pin and output type*/
	LL_GPIO_SetPinMode (GPIOB,LL_GPIO_PIN_7 , LL_GPIO_MODE_OUTPUT);
	LL_GPIO_SetPinMode (GPIOB,LL_GPIO_PIN_14 , LL_GPIO_MODE_OUTPUT);
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_7 , LL_GPIO_MODE_OUTPUT);

	/* Set PC13 as input user button*/
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_13 , LL_GPIO_MODE_INPUT);
	static int i = 1;
	while(1)
	{

		if (LL_GPIO_IsInputPinSet (GPIOC,LL_GPIO_PIN_13 ))
			{
				switch (i){
				case 1:
					LL_GPIO_SetOutputPin (GPIOB,LL_GPIO_PIN_7);
					for(int itr = 0; itr< 90000;itr++){};
					i++;
					break;
				case 2:
					LL_GPIO_SetOutputPin (GPIOB,LL_GPIO_PIN_14);
					for(int itr = 0; itr< 90000;itr++){};
					i++;
					break;
				case 3:
					LL_GPIO_SetOutputPin (GPIOC,LL_GPIO_PIN_7);
					for(int itr = 0; itr< 90000;itr++){};
					i = 1;
					break;
				}

			}
		else
			{
				LL_GPIO_ResetOutputPin (GPIOB,LL_GPIO_PIN_7 | LL_GPIO_PIN_14);
				LL_GPIO_ResetOutputPin (GPIOC,LL_GPIO_PIN_7 );
			}


	}

}
