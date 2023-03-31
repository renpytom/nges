#include <time.h>
#include "nes/nes.h"
#include "nes/cartridge/parse_rom.h"
#include "nes/joy/controllers/standard.h"


/* Parameters for the NES. */
static NES_Params params = {
    .apu_sample_rate = 96000,
    .speed = 100,
    .log_cpu = false,
    .ppu_timing_hack = false,
};

/* The NES. */
NES nes(params);

/* The ROM file. */
ROM_File *rom_file;
Mapper *mapper;

/* The controllers. */
JOY_Standard joy_1 { "P1" };
JOY_Standard joy_2 { "P2" };


/* Called to initialize things. */
extern "C" void init() {
    nes.attach_joy(0, &joy_1);

    // The second controller causes problems in Super Mario Brothers.
    // nes.attach_joy(1, &joy_2);
}

/* Loads a ROM.
*
* rom_data is a pointer to the ROM data.
* rom_size is the size of the ROM data, in bytes.
*
* Returns 0 on success, -1 on failure.
*/
extern "C" int load_rom(void *rom_data, unsigned int rom_size) {

    nes.removeCartridge();

    if (mapper) {
        delete mapper;
        mapper = NULL;
    }


    if (rom_file) {
        delete rom_file;
        rom_file = NULL;
    }

    rom_file = parseROM((u8 *) rom_data, rom_size);

    if (!rom_file) {
        return -1;
    }

    mapper = Mapper::Factory(rom_file);

    if (!mapper) {
        return -1;
    }

    nes.loadCartridge(mapper);
    nes.power_cycle();
    return 0;
}

// For speed reasons, this needs to be a power of two.
static const int AUDIO_QUEUE_SIZE = 2048 * 3;
static const int FILL_THRESHOLD = 2048;

static volatile float audio_queue[AUDIO_QUEUE_SIZE];
static volatile int read_index = 0;
static volatile int write_index = 0;

static int samples_in_queue() {
    if (write_index >= read_index) {
        return write_index - read_index;
    } else {
        return AUDIO_QUEUE_SIZE + write_index - read_index;
    }
}

static float read_sample() {

    if (read_index == write_index) {
        return 0;
    }

    float rv = audio_queue[read_index];
    read_index = (read_index + 1) % AUDIO_QUEUE_SIZE;
    return rv;
}

static void write_sample(float sample) {
    audio_queue[write_index] = sample;
    write_index = (write_index + 1) % AUDIO_QUEUE_SIZE;
}

/* Steps to the next frame. */
extern "C" void step_frame() {

    while ((AUDIO_QUEUE_SIZE - samples_in_queue()) > FILL_THRESHOLD) {
        nes.step_frame();

        float *samples;
        uint sample_count;

        nes.getAudiobuff(&samples, &sample_count);

        for (uint i = 0; i < sample_count; i++) {
            write_sample(samples[i]);
        }
    }
}

extern "C" const unsigned char *get_framebuffer() {
    const unsigned char *framebuffer;

    nes.getFramebuff(&framebuffer);

    return framebuffer;
}

extern "C" void audio(float *buf, int samples) {
    for (int i = 0; i < samples * 2; i++) {
        float sample = read_sample() * .75;
        *buf++ = sample;
    }

}

extern "C" void set_button(int player, int button, int active) {
    if (player == 1) {
        joy_1.set_button((JOY_Standard_Button::Type) button, active);
    } else {
        joy_2.set_button((JOY_Standard_Button::Type) button, active);
    }
}
