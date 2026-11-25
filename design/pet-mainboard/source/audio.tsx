import {speakerHeader} from './layout';
// Coordinates use the carrier layout frame. Passives under the raised XIAO clear its sockets.
const passives = [
  {ref:'R_F1', x:28.0, y:25.3, code:'C25804', mpn:'0603WAF1002T5E', a:'AUDIO_PWM', b:'ATT'},
  {ref:'R_ATT', x:28, y:22.8, code:'C21190', mpn:'0603WAF1001T5E', a:'ATT', b:'GND'},
  {ref:'C_F1', x:24.6, y:25.3, code:'C21122', mpn:'CL10B223KB8NNNC', a:'ATT', b:'GND'},
  {ref:'R_F2', x:24.6, y:22.8, code:'C21190', mpn:'0603WAF1001T5E', a:'ATT', b:'LPF'},
  {ref:'C_F2', x:21.2, y:25.3, code:'C21122', mpn:'CL10B223KB8NNNC', a:'LPF', b:'GND'},
  {ref:'C_INP', x:20.6, y:23.8, code:'C14663', mpn:'CC0603KRX7R9BB104', a:'LPF', b:'COUP_POS'},
  {ref:'R_INP', x:17.7, y:21.9, code:'C22984', mpn:'0603WAF3002T5E', a:'COUP_POS', b:'AMP_P'},
  {ref:'R_INN', x:17.7, y:24.0, code:'C22984', mpn:'0603WAF3002T5E', a:'COUP_NEG', b:'AMP_N'},
  {ref:'C_INN', x:10.2, y:18, code:'C14663', mpn:'CC0603KRX7R9BB104', a:'GND', b:'COUP_NEG'},
  {ref:'R_EN', x:28, y:20.1, code:'C25804', mpn:'0603WAF1002T5E', a:'AUDIO_PWM', b:'AMP_EN'},
  {ref:'C_EN', x:24.6, y:20.1, code:'C15849', mpn:'CL10A105KB8NNNC', a:'AMP_EN', b:'GND'},
  {ref:'R_OFF', x:28, y:17.6, code:'C25804', mpn:'0603WAF1002T5E', a:'AUDIO_PWM', b:'GND'},
  {ref:'C_BYP', x:17.5, y:17, code:'C15849', mpn:'CL10A105KB8NNNC', a:'BYPASS', b:'GND'},
  {ref:'C_VDD', x:13.825, y:25.9, rotation:180, code:'C15849', mpn:'CL10A105KB8NNNC', a:'V3V3', b:'GND'},
  {ref:'C_RF', x:10.2, y:23.0, code:'C1588', mpn:'CL10B102KB8NNNC', a:'V3V3', b:'GND'},
  {ref:'C_BULK', x:10.3, y:20.5, code:'C15850', mpn:'CL21A106KAYNNNE', a:'V3V3', b:'GND'},
  {ref:'C_MIC', x:20.5, y:10.65, code:'C14663', mpn:'CC0603KRX7R9BB104', a:'V3V3', b:'GND'},
];
export const Audio = () => <>
  {passives.map(p => <chip key={p.ref} name={p.ref} pcbX={p.x} pcbY={p.y} pcbRotation={p.rotation ?? 0} layer="top" schSectionName="Audio"
    footprint={`jlcpcb:${p.code}`} manufacturerPartNumber={p.mpn} supplierPartNumbers={{jlcpcb:[p.code]}}
    connections={{pin1:`net.${p.a}`,pin2:`net.${p.b}`}} />)}
  <chip name="MIC1" pcbX={25.4} pcbY={9.5} layer="top" schSectionName="Audio"
    cadModel={{
      stepUrl: "./source/models/LMD4737T261-OAC05.step",
      modelOriginPosition: {x: 0, y: 0, z: 0},
      positionOffset: {x: 0, y: 0, z: 0},
      rotationOffset: {x: 0, y: 0, z: 0},
      modelUnitToMmScale: 1,
      modelBoardNormalDirection: "z+",
    }}
    footprint="jlcpcb:C47148418" manufacturerPartNumber="LMD4737T261-OAC05" supplierPartNumbers={{jlcpcb:['C47148418']}}
    pinLabels={{pin1:'GND1',pin2:'LR',pin3:'GND2',pin4:'CLK',pin5:'DATA',pin6:'VDD'}}
    connections={{GND1:'net.GND',LR:'net.GND',GND2:'net.GND',CLK:'net.MIC_CLK',DATA:'net.MIC_DATA',VDD:'net.V3V3'}} />
  <chip name="U_AMP" pcbX={14.2} pcbY={20.8} layer="top" schSectionName="Audio"
    footprint="jlcpcb:C189961" manufacturerPartNumber="NS4150B" supplierPartNumbers={{jlcpcb:['C189961']}}
    pinLabels={{pin1:'CTRL',pin2:'BYPASS',pin3:'INP',pin4:'INN',pin5:'VON',pin6:'VCC',pin7:'GND',pin8:'VOP'}}
    connections={{CTRL:'net.AMP_EN',BYPASS:'net.BYPASS',INP:'net.AMP_P',INN:'net.AMP_N',VON:'net.SPK_N',VCC:'net.V3V3',GND:'net.GND',VOP:'net.SPK_P'}} />
  <connector name="SPK1" pcbX={speakerHeader.x} pcbY={speakerHeader.y} pcbRotation={speakerHeader.rotation}
    layer="top" schSectionName="Audio" manufacturerPartNumber="532610271"
    supplierPartNumbers={{jlcpcb:['C177225']}} footprint="jlcpcb:C177225"
    schPinArrangement={{topSide:[1,2],bottomSide:[3,4]}} pinLabels={{pin1:'PLUS',pin2:'MINUS',pin3:'TAB1',pin4:'TAB2'}} noConnect={['TAB1','TAB2']} connections={{PLUS:'net.SPK_P',MINUS:'net.SPK_N'}} />
</>;
