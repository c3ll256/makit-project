# TamaGPT Star Pet

TamaGPT is a handheld virtual pet shaped like a five-pointed star. A black circular bezel frames a 1.54-inch square color display with 240 × 240 pixels to draw a blink, a yawn, or a sleepy pair of eyes. The translucent lavender shell measures about 10 cm across. Its two lower points taper toward the tips, and the top point holds a key ring.

Three buttons form a small triangle on the lower-left point. The dark 12 mm main button sits above two 8 mm buttons that match the shell. One corner of the custom circuit board extends under this cluster so each button presses its own switch directly. The lowest button is reserved for voice messages. The plan is to hold it to record a message, then release it to hear the pet play it back.

## Building the hardware

The front and back shells print in translucent PETG and fasten with four screws. Inside, a Seeed Studio XIAO ESP32S3 plugs into a custom two-layer carrier board. The display plugs into an eight-pin header, and the speaker has its own socket. A USB-C port on the right handles charging and programming.

The project includes editable enclosure models, the carrier board design, and PCB fabrication and assembly files. Button travel has been checked in CAD, and the board has passed electrical checks. The first physical build will test button return, screen alignment, and how clearly the microphone and speaker work with the case closed.
