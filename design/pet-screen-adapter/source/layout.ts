export const board={width:20,height:11,thickness:1.0};
const rotationForOpening=(native:number,target:number)=>(target-native+360)%360;
export const socket={x:0,y:-3.5,rotation:0};
export const gh={x:0,y:1.5,rotation:rotationForOpening(270,90)};
