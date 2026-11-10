import {board, outline, keys, header, mountHoles, grove, lcdHeader} from './layout';
import {boardPropsFromRules,groundPourPropsFromRules,netPropsFor,pcbRules,keepoutPropsFromRules} from './lib/makit-pcb';
export default () => (
 <board width={board.width} height={board.height} outline={outline} thickness={board.thickness} {...boardPropsFromRules()}>
  {Object.keys(pcbRules.nets).map(n=><net key={n} name={n} {...netPropsFor(n)}/>)}
  {groundPourPropsFromRules().map(p=><copperpour key={p.name} {...p}/>)}
  {keepoutPropsFromRules().map(k=><keepout key={k.name} {...k}/>)}
  {keys.map(k=><chip key={k.ref} name={k.ref} footprint="jlcpcb:C110153" manufacturerPartNumber="K2-1102DP-C4SW-04" cadModel={{stepUrl:"./source/models/SW_PUSH_6mm_H5mm.step",modelOriginPosition:{x:3.25,y:-2.25,z:0},positionOffset:{x:0,y:0,z:0},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}} pcbX={k.x} pcbY={k.y} layer="top" schSectionName="Keys" pinLabels={{pin1:'KEY_A',pin2:'KEY_B',pin3:'GND_A',pin4:'GND_B'}} internallyConnectedPins={[[1,2],[3,4]]} connections={{KEY_A:`net.${k.net}`,KEY_B:`net.${k.net}`,GND_A:'net.GND',GND_B:'net.GND'}} />)}
  <trace from=".SW_RIGHT > .KEY_A" to=".SW_RIGHT > .KEY_B" />
  <connector name="J_KEYS" doNotPlace footprint="jlcpcb:C32713270" manufacturerPartNumber="HX PZ2.54-1x4P ZZ" pcbX={header.x} pcbY={header.y} pcbRotation={header.rotation} layer="bottom" schSectionName="Keys" pinLabels={{pin1:'GND',pin2:'LEFT_D0',pin3:'MID_D1',pin4:'RIGHT_D3'}} connections={{GND:'net.GND',LEFT_D0:'net.KEY_LEFT',MID_D1:'net.KEY_MID',RIGHT_D3:'net.KEY_RIGHT'}} />
  <connector name="J_GROVE" footprint="jlcpcb:C7429589" manufacturerPartNumber="ZX-HY2.0-4PWZ" pcbX={grove.x} pcbY={grove.y} pcbRotation={grove.rotation} layer="bottom" schSectionName="Display" pinLabels={{pin1:'GND',pin2:'V3V3',pin3:'DATA',pin4:'SCK'}} connections={{SCK:'net.LCD_SCK',DATA:'net.LCD_DATA',V3V3:'net.V3V3',GND:'net.GND'}} />
  <connector name="J_LCD_MCU" doNotPlace footprint="jlcpcb:C32713270" manufacturerPartNumber="HX PZ2.54-1x4P ZZ" pcbX={lcdHeader.x} pcbY={lcdHeader.y} pcbRotation={lcdHeader.rotation} layer="bottom" schSectionName="Display" pinLabels={{pin1:'GND',pin2:'V3V3',pin3:'D10_DATA',pin4:'D9_SCK'}} connections={{GND:'net.GND',V3V3:'net.V3V3',D10_DATA:'net.LCD_DATA',D9_SCK:'net.LCD_SCK'}} />
  <silkscreentext text="LCD 3V3" pcbX={10} pcbY={-2.0} fontSize={1} layer="bottom"/>
  {keys.map(k=><silkscreentext key={k.ref} text={k.net.replace('KEY_','')} pcbX={k.x} pcbY={k.y+4.2} fontSize={0.8} layer="top"/>)}
  {['G','L','M','R'].map((t,i)=><silkscreentext key={t} text={t} pcbX={-6.19-i*2.54} pcbY={10.4} fontSize={0.8} layer="bottom"/>)}
  {mountHoles.map((p,i)=><hole key={i} name={`MH${i+1}`} diameter={2.2} pcbX={p.x} pcbY={p.y}/>)}
 </board>
);
