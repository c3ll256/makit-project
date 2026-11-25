import shellOutline from './components/outline.json';
// The rounded lower-left extension carries three direct-acting keys below the speaker.
// Source coordinates use the enclosure frame, with the USB port toward +X.
export const board={width:68.5,height:48.25,thickness:1};
export const shellOffset={x:0,y:-21.5,zTop:4.74};
export const outline=shellOutline.map(([x,y])=>({x,y:y+21.5}));
// The switch centres are the three marks in enclosure XY. The PCB frame is 21.5 mm higher in Y.
export const keys = [
  {ref:'SW_LEFT', x:-28.25, y:1, rotation:0, net:'KEY_LEFT'},
  {ref:'SW_MID', x:-32.25, y:-11.5, rotation:0, net:'KEY_MID'},
  {ref:'SW_RIGHT', x:-19, y:-6.5, rotation:0, net:'KEY_RIGHT'},
];
export const mountHoles=[{x:7.5,y:-0.5},{x:-7.5,y:-0.5}];
// Header rows from Seeed DIP footprint: 15.24 mm between rows, 2.54 mm pitch.
// Pin 1 at the USB (+X) end. +Y row D0..D6; -Y row VBUS/GND/3V3/D10/D9/D8/D7.
export const xiao={x:20.2153588244,y:21.5,stack:6.0,rotation:0};
export const sockets=[
 {ref:'J_XIAO_A',x:xiao.x-1.27,y:xiao.y+7.62,rotation:180,code:'C2915256',mpn:'MF254V-11-08-0540',labels:{pin1:'D0',pin2:'D1',pin3:'D2',pin4:'D3',pin5:'D4',pin6:'D5',pin7:'D6',pin8:'SPARE_A'},connections:{D0:'net.AUDIO_PWM',D1:'net.MIC_DATA',D2:'net.MIC_CLK',D3:'net.KEY_RIGHT',D4:'net.LCD_RES',D5:'net.LCD_DC',D6:'net.LCD_BLK'},noConnect:['SPARE_A']},
 {ref:'J_XIAO_B',x:xiao.x-1.27,y:xiao.y-7.62,rotation:180,code:'C2915256',mpn:'MF254V-11-08-0540',labels:{pin1:'VBUS',pin2:'GND',pin3:'V3V3',pin4:'D10',pin5:'D9',pin6:'D8',pin7:'D7',pin8:'SPARE_B'},connections:{GND:'net.GND',V3V3:'net.V3V3',D10:'net.LCD_DATA',D8:'net.LCD_SCK',D7:'net.KEY_LEFT',D9:'net.KEY_MID'},noConnect:['VBUS','SPARE_B']}
];
// XIAO USB faces right; both peripheral plugs have dedicated carrier footprints.
export const lcd={x:0,y:6.99,rotation:180};
export const speakerHeader={x:-14.9,y:7.35,rotation:90};
