# Switch mechanical model

SW_PUSH_6mm_H5mm.step is copied unchanged from the installed KiCad Button_Switch_THT.3dshapes library. Official upstream: https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Button_Switch_THT.3dshapes/SW_PUSH_6mm_H5mm.step

SHA256: 4461bd8b9765c0569a962e3d7bf254d3f2785ff83e20b087ee0469fb2f89fe2c

This standard 6 mm switch model represents the selected C110153 supplier drawing's 5 mm above-board height and 6.5 x 4.5 mm pin pattern. The supplier-supplied model instead showed a taller actuator. It is a dimensional stand-in, not a new electrical part. Source JSX binds board-surface offset zero; KiCad supplies the board thickness. The model actuator centre is offset 0.1 mm in X; cap socket has 0.2 mm radial clearance. Applicable KiCad model-library licence: see upstream LICENSE.md and exception; retained upstream attribution in STEP header.

## XIAO direct plug update
Official Seeed XIAO ESP32-S3 STEP from https://files.seeedstudio.com/wiki/SeeedStudio-XIAO-ESP32S3/res/seeed-studio-xiao-esp32s3-3d_model.zip , entry XIAO-ESP32S3 v2.step, sha256 870ad45c7af5d92324cec4c6ae65fbf86e3b049d5a97ab9ffd9039ebd73455dd. Archive dated 2023-05-27; licence not stated in archive. Coordinate normal +Y becomes +Z by X=90 degrees; origin at pin-row centre (1.740658685586,-0.249999985099,-6.111399955413). Exact ESP32-S3, not other XIAO variants. Row pitch/spacing from official XIAO-ESP32-S3-DIP footprint archive, 2.54 / 15.24 mm; vendor DIP drill is not used for carrier holes.

Round male header STEP URLs are resolved from the exact C509261 and C2844842 supplier footprints. Body-only parts sit 3 mm above carrier; they carry no duplicate copper. Female C2915256 uses supplier footprint/model. Datasheet drawings in supplier lookup records establish 3 mm body heights.
