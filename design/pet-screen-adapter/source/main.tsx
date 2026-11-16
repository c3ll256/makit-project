import {board,socket,gh} from "./layout";
import {boardPropsFromRules,groundPourPropsFromRules,netPropsFor,pcbRules} from "./lib/makit-pcb";
export default()=> (<board width={board.width} height={board.height} thickness={board.thickness} {...boardPropsFromRules()}>
{Object.keys(pcbRules.nets).map(n=><net key={n} name={n} {...netPropsFor(n)}/>)}
{groundPourPropsFromRules().map(p=><copperpour key={p.name} {...p}/>)}
<connector name="J_SCREEN" footprint="jlcpcb:C27985232" manufacturerPartNumber="HC-PM254-5.0H-1x7PZ" layer="bottom" pcbX={socket.x} pcbY={socket.y} pcbRotation={socket.rotation} pinLabels={{pin1:'GND',pin2:'V3V3',pin3:'SCK',pin4:'DATA',pin5:'RES',pin6:'DC',pin7:'BLK'}} connections={{GND:'net.GND',V3V3:'net.V3V3',SCK:'net.LCD_SCK',DATA:'net.LCD_DATA',RES:'net.LCD_RES',DC:'net.LCD_DC',BLK:'net.LCD_BLK'}}/>
<connector name="J_SCREEN_GH" noConnect={["pin8","pin9"]} footprint="jlcpcb:C495552" manufacturerPartNumber="SM07B-GHS-TB(LF)(SN)" supplierPartNumbers={{jlcpcb:["C495552"]}} layer="top" pcbX={gh.x} pcbY={gh.y} pcbRotation={gh.rotation} pinLabels={{pin1:'GND',pin2:'V3V3',pin3:'SCK',pin4:'DATA',pin5:'RES',pin6:'DC',pin7:'BLK'}} connections={{GND:'net.GND',V3V3:'net.V3V3',SCK:'net.LCD_SCK',DATA:'net.LCD_DATA',RES:'net.LCD_RES',DC:'net.LCD_DC',BLK:'net.LCD_BLK'}}/>
</board>);
