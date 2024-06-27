#include "pico/stdlib.h"
#include "hardware/adc.h"
#include <stdio.h>

// Define the control pins for the multiplexer
#define MUX_CONTROL_PIN0 12
#define MUX_CONTROL_PIN1 13
#define MUX_CONTROL_PIN2 14
#define MUX_CONTROL_PIN3 15
#define MUX_CONTROL_PIN4 26

// Define the ADC pin connected to the output of the multiplexer
#define MUX_ADC_PIN 27

void select_mux_channel(uint8_t channel) {
    gpio_put(MUX_CONTROL_PIN0, channel & 0x01);
    gpio_put(MUX_CONTROL_PIN1, (channel >> 1) & 0x01);
    gpio_put(MUX_CONTROL_PIN2, (channel >> 2) & 0x01);
    gpio_put(MUX_CONTROL_PIN3, (channel >> 3) & 0x01);
    gpio_put(MUX_CONTROL_PIN4, (channel >> 4) & 0x01);
}

uint16_t read_sensor(uint8_t channel) {
    // Select the multiplexer channel
    select_mux_channel(channel);
    
    // Allow some time for the multiplexer to settle
    sleep_us(10);
    
    // Read the analog value from the ADC
    uint16_t result = adc_read();
    return result;
}

int main() {
    stdio_init_all();
    
    // Initialize the ADC
    adc_init();
    
    // Set the ADC pin
    adc_gpio_init(MUX_ADC_PIN);
    adc_select_input(0);  // Assuming ADC0 is connected to the multiplexer output

    // Initialize the multiplexer control pins as output
    gpio_init(MUX_CONTROL_PIN0);
    gpio_set_dir(MUX_CONTROL_PIN0, GPIO_OUT);
    gpio_init(MUX_CONTROL_PIN1);
    gpio_set_dir(MUX_CONTROL_PIN1, GPIO_OUT);
    gpio_init(MUX_CONTROL_PIN2);
    gpio_set_dir(MUX_CONTROL_PIN2, GPIO_OUT);
    gpio_init(MUX_CONTROL_PIN3);
    gpio_set_dir(MUX_CONTROL_PIN3, GPIO_OUT);
    gpio_init(MUX_CONTROL_PIN4);
    gpio_set_dir(MUX_CONTROL_PIN4, GPIO_OUT);
    
    while (1) {
        for (uint8_t channel = 0; channel < 29; ++channel) {
            uint16_t sensor_value = read_sensor(channel);
            printf("Sensor %d: %u\n", channel, sensor_value);
            sleep_ms(100);  // Delay between readings
        }
    }
    
    return 0;
}

