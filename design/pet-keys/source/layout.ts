// XY matches pet-shell, translated +21.5 mm along Y. Nominal board top in shell at Z=14.1.
// Fixed button centres come from button_ring_radius=27.5 in pet-shell.
export const board = { width: 59, height: 26.5, thickness: 1.6 };
export const shellOffset = { x: 0, y: -21.5, zTop: 14.1 };
const bossNotch=(x:number)=>Array.from({length:17},(_,i)=>({x:x+3.6*Math.cos(i*Math.PI/16),y:-0.2+3.6*Math.sin(i*Math.PI/16)}));
export const outline = [
{x:-29.5,y:13},{x:29.5,y:13},{x:29.5,y:2},...bossNotch(22.5),{x:17,y:-3},{x:16.5,y:-5.5},{x:13.5,y:-8.5},{x:7,y:-13.5},{x:-7,y:-13.5},{x:-13,y:-8.5},{x:-17,y:-3},...bossNotch(-22.5),{x:-29.5,y:1}
];
export const keys = [
 {ref:'SW_LEFT',x:-27.5*Math.sqrt(3)/2,y:7.75,net:'KEY_LEFT'},
 {ref:'SW_MID',x:0,y:-6,net:'KEY_MID'},
 {ref:'SW_RIGHT',x:27.5*Math.sqrt(3)/2,y:7.75,net:'KEY_RIGHT'}
];
// Switches front; header footprints DNP with low-profile wire pigtails.
export const header = {x:-10,y:8,rotation:0};
export const mountHoles = [{x:0,y:-11},{x:-9,y:-9}];

// Grove rear central bridge; cable runs over battery through the lowered tray notch.
export const grove = {x:10,y:-5,rotation:180,nativeOpening:"down",targetOpening:"up"};
export const lcdHeader = {x:-8,y:0,rotation:180};
