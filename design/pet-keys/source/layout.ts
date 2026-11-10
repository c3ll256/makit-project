// Board XY equals shell XY + (0,21.5); carrier top Z4.740 mm.
export const board = { width: 52.5, height: 45.5, thickness: 1.6 };
export const shellOffset = {x:0,y:-21.5,zTop:4.740};
const P=(x:number,y:number)=>({x,y:y+21.5});
const rightBoss=Array.from({length:17},(_,i)=>P(24+3.6*Math.cos(i*Math.PI/16),-20+3.6*Math.sin(i*Math.PI/16)));
const stop=Math.asin(2.3/3.6);
const leftBoss=Array.from({length:7},(_,i)=>P(-24+3.6*Math.cos(i*stop/6),-20+3.6*Math.sin(i*stop/6)));
const topBoss=Array.from({length:13},(_,i)=>{const a=-Math.PI+Math.asin(2.5/3.5)+(Math.PI-2*Math.asin(2.5/3.5))*i/12;return P(27+3.5*Math.cos(a),13+3.5*Math.sin(a));});
export const outline=[P(-24+Math.sqrt(3.6**2-2.3**2),-17.7),P(7.5,-17.7),P(7.5,10.5),...topBoss,P(31,10.5),P(31,-12),P(29.5,-17.5),P(29.5,-20),...rightBoss,P(21.5,-24.5),P(18,-26.5),P(13,-29.7),P(7,-35),P(-7,-35),P(-13,-29.7),P(-18,-26.5),P(-21.5,-24.5),...leftBoss.slice(0,-1)];
export const keys=[{ref:'SW_LEFT',x:-14.5,y:-2,rotation:-35,net:'KEY_LEFT'},{ref:'SW_MID',x:0,y:-5,rotation:0,net:'KEY_MID'},{ref:'SW_RIGHT',x:14.5,y:-2,rotation:35,net:'KEY_RIGHT'}];
export const mountHoles=[{x:0,y:-11},{x:-9,y:-9}];
// Header rows from Seeed DIP footprint: 15.24 mm between rows, 2.54 mm pitch.
// Pin 1 at the USB (+X) end. +Y row D0..D6; -Y row VBUS/GND/3V3/D10/D9/D8/D7.
export const xiao={x:20.2153588244,y:21.5,stack:6.0,rotation:0};
export const sockets=[
 {ref:'J_XIAO_A',x:xiao.x-1.27,y:xiao.y+7.62,rotation:180,code:'C2915256',mpn:'MF254V-11-08-0540',labels:{pin1:'D0',pin2:'D1',pin3:'D2',pin4:'D3',pin5:'D4',pin6:'D5',pin7:'D6',pin8:'SPARE_A'},connections:{D3:'net.KEY_RIGHT',D4:'net.LCD_RES',D5:'net.LCD_DC',D6:'net.LCD_BLK'},noConnect:['D0','D1','D2','SPARE_A']},
 {ref:'J_XIAO_B',x:xiao.x-1.27,y:xiao.y-7.62,rotation:180,code:'C2915256',mpn:'MF254V-11-08-0540',labels:{pin1:'VBUS',pin2:'GND',pin3:'V3V3',pin4:'D10',pin5:'D9',pin6:'D8',pin7:'D7',pin8:'SPARE_B'},connections:{GND:'net.GND',V3V3:'net.V3V3',D10:'net.LCD_DATA',D8:'net.LCD_SCK',D7:'net.KEY_LEFT',D9:'net.KEY_MID'},noConnect:['VBUS','SPARE_B']}
];
// Vertical screen cable connector outside XIAO and above the key group.
export const lcd={x:20.2,y:8.5,rotation:180};
