#include "stm32l4xx_ll_bus.h"
#include "stm32l4xx_ll_gpio.h"




int main(){



	/* Enable clock for GPIOC first*/
	LL_AHB2_GRP1_EnableClock (LL_AHB2_GRP1_PERIPH_GPIOC);


	/* Now declare pin PC7 as output pin*/
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_7 , LL_GPIO_MODE_OUTPUT);

	/* Set PC13 as input pin */
	LL_GPIO_SetPinMode (GPIOC,LL_GPIO_PIN_13 , LL_GPIO_MODE_INPUT);

	/* if push button is pressed LED will be reset else  it will be set */
	while(1){

		if (LL_GPIO_IsInputPinSet (GPIOC,  LL_GPIO_PIN_13)){

			LL_GPIO_ResetOutputPin (GPIOC,LL_GPIO_PIN_7 );
		}
		else{

			LL_GPIO_SetOutputPin (GPIOC,LL_GPIO_PIN_7 );
		}

//		LL_GPIO_TogglePin (GPIOC, LL_GPIO_PIN_7);
//		for(int itr = 0; itr<90000;itr++){}

	}





	return 0;
}
