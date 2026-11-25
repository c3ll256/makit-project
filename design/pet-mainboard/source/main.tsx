import {Audio} from './audio';
import {board, outline, keys, mountHoles, lcd, sockets, xiao} from './layout';
import {boardPropsFromRules,groundPourPropsFromRules,netPropsFor,pcbRules,keepoutPropsFromRules} from './lib/makit-pcb';
export default () => (
 <board width={board.width} height={board.height} outline={outline} thickness={board.thickness} {...boardPropsFromRules()}>
  {Object.keys(pcbRules.nets).map(n=><net key={n} name={n} {...netPropsFor(n)}/>)}
  {groundPourPropsFromRules().map(p=><copperpour key={p.name} {...p}/>)}
  {keepoutPropsFromRules().map(k=><keepout key={k.name} {...k}/>)}
  {keys.map(k=><chip key={k.ref} name={k.ref} footprint="jlcpcb:C110153" manufacturerPartNumber="K2-1102DP-C4SW-04" cadModel={{stepUrl:"./source/models/SW_PUSH_6mm_H5mm.step",modelOriginPosition:{x:3.25,y:-2.25,z:0},positionOffset:{x:0,y:0,z:0},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}} pcbX={k.x} pcbY={k.y} pcbRotation={k.rotation} layer="top" schSectionName="Keys" pinLabels={{pin1:'KEY_A',pin2:'KEY_B',pin3:'GND_A',pin4:'GND_B'}} connections={{KEY_A:`net.${k.net}`,KEY_B:`net.${k.net}`,GND_A:'net.GND',GND_B:'net.GND'}} />)}
  {keys.map(k=><trace key={k.ref} name={`${k.ref}_common`} from={`.${k.ref} > .KEY_A`} to={`.${k.ref} > .KEY_B`} />)}
  <connector name="J_SCREEN" footprint="jlcpcb:C2897371" manufacturerPartNumber="PM254-1-08-Z-8.5" supplierPartNumbers={{jlcpcb:["C2897371"]}} pcbX={lcd.x} pcbY={lcd.y} pcbRotation={lcd.rotation} layer="top" schSectionName="Display" connections={{pin1:"net.GND",pin2:"net.V3V3",pin3:"net.LCD_SCK",pin4:"net.LCD_DATA",pin5:"net.LCD_RES",pin6:"net.LCD_DC",pin7:"net.GND",pin8:"net.LCD_BLK"}}/>
  <silkscreentext text="GND" pcbX={8.89} pcbY={4.62} fontSize={0.75} layer="top"/>
  <silkscreentext text="BLK" pcbX={-8.89} pcbY={4.62} fontSize={0.75} layer="top"/>
  {keys.map(k=><silkscreentext key={k.ref} text={k.net.replace('KEY_','')} pcbX={k.x} pcbY={k.y-4.05} fontSize={0.65} layer="top"/>)}
  {sockets.map(s=><connector key={s.ref} name={s.ref} footprint={`jlcpcb:${s.code}`} manufacturerPartNumber={s.mpn} pcbX={s.x} pcbY={s.y} pcbRotation={s.rotation} layer="top" schSectionName="XIAO" pinLabels={s.labels} connections={s.connections} noConnect={s.noConnect}/>)}
  <chip name="P_XIAO_A4" footprint={<footprint/>} manufacturerPartNumber="MH254V-11-04-1000" pcbX={24.0253588244} pcbY={29.12} pcbRotation={180} layer="top" schSectionName="Assembly bodies" cadModel={{stepUrl:"https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/342bb6b6334547d8b3fc71eb07c1abf9",modelOriginPosition:{x:0.0005381,y:-1.27e-05,z:0.499993},positionOffset:{x:0,y:0,z:3},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}}/>
  <chip name="P_XIAO_A3" footprint={<footprint/>} manufacturerPartNumber="MH254V-11-03-1000" pcbX={15.1353588244} pcbY={29.12} pcbRotation={180} layer="top" schSectionName="Assembly bodies" cadModel={{stepUrl:"https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/bc500d46b25542d58136a3d763742d6e",modelOriginPosition:{x:0.0001008,y:0,z:0.0749936},positionOffset:{x:0,y:0,z:2.7},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}}/>
  <chip name="P_XIAO_B4" footprint={<footprint/>} manufacturerPartNumber="MH254V-11-04-1000" pcbX={24.0253588244} pcbY={13.88} pcbRotation={180} layer="top" schSectionName="Assembly bodies" cadModel={{stepUrl:"https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/342bb6b6334547d8b3fc71eb07c1abf9",modelOriginPosition:{x:0.0005381,y:-1.27e-05,z:0.499993},positionOffset:{x:0,y:0,z:3},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}}/>
  <chip name="P_XIAO_B3" footprint={<footprint/>} manufacturerPartNumber="MH254V-11-03-1000" pcbX={15.1353588244} pcbY={13.88} pcbRotation={180} layer="top" schSectionName="Assembly bodies" cadModel={{stepUrl:"https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/bc500d46b25542d58136a3d763742d6e",modelOriginPosition:{x:0.0001008,y:0,z:0.0749936},positionOffset:{x:0,y:0,z:2.7},rotationOffset:{x:0,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}}/>
  <chip name="U_XIAO" footprint={<footprint/>} manufacturerPartNumber="Seeed Studio XIAO ESP32-S3" pcbX={xiao.x} pcbY={xiao.y} layer="top" schSectionName="Assembly bodies" cadModel={{stepUrl:"./source/models/xiao-esp32s3.step",modelOriginPosition:{x:1.740658685586,y:-0.2499999850988,z:-6.111399955413},positionOffset:{x:0,y:0,z:xiao.stack},rotationOffset:{x:-90,y:0,z:0},modelUnitToMmScale:1,modelBoardNormalDirection:"z+"}}/>
  <Audio/>
  {mountHoles.map((p,i)=><hole key={i} name={`MH${i+1}`} diameter={2.4} pcbX={p.x} pcbY={p.y}/>)}
 </board>
);
